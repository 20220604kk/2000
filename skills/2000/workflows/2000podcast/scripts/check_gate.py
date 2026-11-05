"""Verify evidence/version prerequisites; never perform or invent the actual reviews."""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

ROLES = {'draft_snapshot', 'video', 'audio', 'cc', 'lower_bar', 'cover_template'}

def file_sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def finite_number(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)

def inspect(report_path):
    report = load(report_path)
    if not isinstance(report, dict):
        raise ValueError('Report must be a JSON object.')
    issues = []
    if report.get('schema_version') != 2:
        issues.append('Use schema_version2; do not silently reinterpret legacy episode reports.')
    checks = report.get('checks', [])
    if not isinstance(checks, list) or any(not isinstance(row, dict) for row in checks):
        raise ValueError('checks must be a list of objects.')
    ids = [row.get('id') for row in checks]
    if len(ids) != 25 or set(ids) != {f'{i:02}' for i in range(1, 26)}:
        issues.append('Each check01..25 must appear exactly once.')
    waiver = report.get('waivers', {}).get('24', {})
    exempt = {'24'} if (waiver.get('approved_by') == 'user' and str(waiver.get('reason', '')).strip()
                        and any(row.get('id') == '24' and row.get('status') == 'waived' for row in checks)) else set()
    if set(report.get('waivers', {})) - {'24'}:
        issues.append('Only the documented user waiver24 is supported; inspect changed acceptance scope.')
    for row in checks:
        if row.get('id') in exempt:
            continue
        if row.get('status') != 'pass':
            issues.append(f'{row.get("id")}: {row.get("status", "missing")}')
        elif not str(row.get('evidence', '')).strip():
            issues.append(f'{row.get("id")}: no evidence description')
    roles = report.get('artifact_roles', {})
    hashes = report.get('artifacts_sha256', {})
    if not isinstance(roles, dict) or not isinstance(hashes, dict):
        raise ValueError('Artifact roles and hashes must be JSON objects.')
    for role in sorted(ROLES):
        if not roles.get(role) or roles[role] not in hashes:
            issues.append(f'{role}: missing versioned artifact')
    if not hashes:
        issues.append('No artifact fingerprints.')
    verified = {}
    def verify_hash(name, expected, label):
        path = Path(name)
        if not path.is_absolute():
            issues.append(f'{label}: absolute artifact path required: {name}')
            return
        if not path.is_file():
            issues.append(f'{label}: missing file: {name}')
            return
        if name not in verified:
            verified[name] = file_sha(path)
        if verified[name] != expected:
            issues.append(f'{label}: file changed: {name}')
    for name, expected in hashes.items():
        verify_hash(name, expected, 'artifact')
    if report.get('actual_export_semantically_matches_latest_draft') is not True:
        issues.append('Latest draft semantic match has not been confirmed.')
    evidence_files = set()
    for ident in sorted({'23', '24', '25'} - exempt):
        review = report.get('reviews', {}).get(ident, {})
        files = review.get('evidence_files', [])
        evidence_hashes = review.get('evidence_sha256', {})
        if review.get('approved') is not True:
            issues.append(f'{ident}: actual review is not approved')
        if not files or not isinstance(files, list):
            issues.append(f'{ident}: actual evidence files are missing')
            files = []
        if review.get('artifacts_sha256') != hashes or not hashes:
            issues.append(f'{ident}: review identifies different artifact versions')
        for name in files:
            evidence_files.add(name)
            if name not in evidence_hashes:
                issues.append(f'{ident}: evidence fingerprint missing: {name}')
            else:
                verify_hash(name, evidence_hashes[name], ident)
    data = {}
    for key in ['visual_review', 'integrity', 'camera_sync', 'audio_sync']:
        name = report.get('video_evidence', {}).get(key)
        if not name or name not in evidence_files:
            issues.append(f'{key}: missing reviewed evidence')
            continue
        try:
            data[key] = load(name)
        except (ValueError, OSError) as error:
            issues.append(f'{key}: unreadable evidence: {error}')
    visual = data.get('visual_review', {})
    if not isinstance(visual, dict) or not (visual.get('approved') is True and visual.get('cc_not_burned_in') is True
                                          and visual.get('reviewed_file') == roles.get('video')):
        issues.append('Actual exported video visual/CC signoff is missing or targets another file.')
    integrity = data.get('integrity', {})
    if not isinstance(integrity, dict):
        integrity = {}
    count = integrity.get('expected_frames')
    if not (isinstance(count, int) and not isinstance(count, bool) and count > 0
            and integrity.get('all_output_frames_decoded') == count
            and integrity.get('decode_errors') is False and integrity.get('subtitle_stream_count') == 0):
        issues.append('Whole-file decode/frame count/subtitle-stream checks have not passed.')
    streams = integrity.get('mp4_probe', {}).get('streams', [])
    video = [s for s in streams if s.get('codec_type') == 'video']
    audio = [s for s in streams if s.get('codec_type') == 'audio']
    if len(streams) != 2 or len(video) != 1 or len(audio) != 1:
        issues.append('Expected exactly one video and one audio stream.')
    else:
        v, a = video[0], audio[0]
        if (v.get('width'), v.get('height'), v.get('r_frame_rate'), v.get('codec_name')) != (1920, 1080, '60/1', 'h264'):
            issues.append('MP4 video format differs from the agreed format.')
        if (a.get('codec_name'), a.get('sample_rate'), a.get('channels')) != ('aac', '44100', 2):
            issues.append('MP4 audio format differs from the agreed format.')
    mp3 = integrity.get('mp3_probe', {}).get('streams', [])
    if len(mp3) != 1 or (mp3[0].get('codec_name'), mp3[0].get('sample_rate'), mp3[0].get('channels'), mp3[0].get('bit_rate')) != ('mp3', '44100', 2, '192000'):
        issues.append('MP3 format differs from the agreed format.')
    peaks = integrity.get('audio', [])
    if not isinstance(peaks, list) or len(peaks) < 2 or any(not isinstance(row, dict)
            or not finite_number(row.get('max_decoded_peak_dbfs')) or row['max_decoded_peak_dbfs'] >= 0 for row in peaks):
        issues.append('Encoded audio peak measurements are missing, invalid or clipping.')
    if 'black_intervals' not in integrity or (integrity.get('black_intervals') and integrity.get('black_intervals_reviewed') is not True):
        issues.append('Black-frame scan is missing or detected intervals have not been reviewed.')
    try:
        snapshot = load(roles['draft_snapshot'])
        duration = snapshot['duration'] / 1e6
        vd = float(integrity['mp4_probe']['format']['duration'])
        ad = float(integrity['mp3_probe']['format']['duration'])
        if not all(finite_number(t) and t > 0 for t in [duration, vd, ad]) or abs(vd-duration) >= .1 or abs(ad-vd) >= .1:
            issues.append('Final media duration does not match the captured timeline.')
        if count != round(duration * 60):
            issues.append('Expected frame count does not match the captured60fps timeline.')
    except (OSError, ValueError, KeyError, TypeError):
        issues.append('Snapshot/media duration evidence is missing or invalid.')
    cameras = data.get('camera_sync', [])
    if not isinstance(cameras, list) or not cameras or any(not isinstance(row, dict) for row in cameras):
        cameras = []
    if any(sum(row.get('camera') == cam for row in cameras) < 3 for cam in ['A', 'B']):
        issues.append('Camera synchronization must include at least head/middle/tail for each camera.')
    if any(not finite_number(row.get('source_residual_seconds')) or abs(row['source_residual_seconds']) >= .04 for row in cameras):
        issues.append('Camera synchronization has invalid or >=40ms residuals.')
    encoded = data.get('audio_sync', [])
    if not isinstance(encoded, list) or any(not isinstance(row, dict) for row in encoded):
        encoded = []
    if any(sum(row.get('file') == ext for row in encoded) < 3 for ext in ['mp4', 'mp3']):
        issues.append('Encoded audio synchronization evidence is insufficient.')
    if any(not finite_number(row.get('residual_seconds')) or abs(row['residual_seconds']) >= .003
           or not finite_number(row.get('correlation')) or row['correlation'] <= .85 for row in encoded):
        issues.append('Encoded audio has invalid residuals or weak correlation.')
    required_total = 25 - len(exempt)
    passed = sum(row.get('status') == 'pass' and row.get('id') not in exempt for row in checks)
    return {'thumbnail_gate_open': not issues, 'required_passed': passed,
            'required_total': required_total, 'waived': sorted(exempt),
            'recorded_pass_percent': round(100 * passed / required_total, 2),
            'verified_percent': 100.0 if not issues else None, 'issues': issues}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report')
    parser.add_argument('--output')
    args = parser.parse_args()
    try:
        result = inspect(args.report)
    except (ValueError, OSError, TypeError, AttributeError, KeyError) as error:
        result = {'thumbnail_gate_open': False, 'verified_percent': None, 'issues': [f'Invalid report: {error}']}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        Path(args.output).write_text(text + '\n', encoding='utf-8')
    return 0 if result['thumbnail_gate_open'] else 2

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
