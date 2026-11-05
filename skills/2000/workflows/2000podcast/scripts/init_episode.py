"""Create episode-specific work files and an optional read-only media inventory."""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

CRITERIA = [
    '畫布與交付規格', '角色軌層及覆蓋順序', 'V1 A右、V2 B左',
    '遮罩方向與接縫', '全部B分檔構圖及調色', 'B分檔連續覆蓋',
    '雙機與錄音同步', '相機原音關閉', '主錄音及片頭片尾聲音',
    '正式節目裁切及音樂', '指定片頭廣告', '指定片尾影片',
    '完整帶影音連續與總長', '本集底BAR內容', '底BAR覆蓋與層次',
    '正式節目逐字稿範圍', 'SRT格式及草稿逐段一致', '繁體與已確認詞',
    '完成帶無壓CC及獨立字幕', '諮商室預設資產', '諮商室定位與動畫',
    '本集全部提問與版型', '最終實際畫面驗收', '完整逐字稿逐句聽校',
    '最終完整帶影音輸出驗收',
]
EXTENSIONS = {'.mp4', '.mov', '.mts', '.m2ts', '.mxf', '.mkv', '.avi',
              '.wav', '.mp3', '.m4a', '.flac'}

def inventory(folder, executable):
    records = []
    flags = (subprocess.CREATE_NO_WINDOW | subprocess.BELOW_NORMAL_PRIORITY_CLASS) if os.name == 'nt' else 0
    for path in sorted(folder.iterdir(), key=lambda p: p.name.casefold()):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        stat = path.stat()
        row = {'path': str(path), 'bytes': stat.st_size, 'mtime_ns': stat.st_mtime_ns}
        try:
            proc = subprocess.run([
                executable, '-v', 'error', '-show_entries',
                'format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,pix_fmt,sample_rate,channels,bit_rate,duration',
                '-of', 'json', str(path)], capture_output=True, text=True,
                encoding='utf-8', errors='replace', timeout=45, creationflags=flags)
            if proc.returncode:
                raise ValueError(proc.stderr.strip() or f'ffprobe exit {proc.returncode}')
            row['probe'] = json.loads(proc.stdout)
        except (ValueError, subprocess.TimeoutExpired, OSError) as error:
            row['error'] = str(error)
        records.append(row)
    return records

def initialize(episode, media_dir, work_dir, probe=False, ffprobe='ffprobe'):
    if episode <= 0:
        raise ValueError('Episode must be positive.')
    media = Path(media_dir).resolve()
    work = Path(work_dir).resolve()
    if not media.is_dir():
        raise ValueError(f'Media directory does not exist: {media}')
    names = ['episode-config.json', f'{episode}_完整性檢查.json']
    if probe:
        names.append('media-inventory.json')
    if any((work / name).exists() for name in names):
        raise ValueError('Existing episode work files found; inspect and resume them instead of initializing again.')
    rows = None
    if probe:
        executable = shutil.which(ffprobe)
        if executable is None:
            raise ValueError(f'ffprobe is unavailable: {ffprobe}')
        rows = inventory(media, executable)
    root = Path(os.environ.get('CAR2000_MEDIA_ROOT', str(media)))
    config = {
        'episode': episode, 'media_dir': str(media), 'draft_name': f'ep{episode}',
        'draft_snapshot': str(work / 'draft-snapshot.json'),
        'sources': {'a_cam': None, 'b_cam_in_verified_order': [], 'main_audio': None},
        'formal_source_range_seconds': None, 'confirmed_title': None,
        'confirmed_terms': {}, 'track_roles': {},
        'references': {'draft': 'ep157', 'intro': str(root / '兩千中古車收車廣告.mp4'),
                       'outro': str(root / 'podcast片尾音樂.mp4'),
                       'lower_bar_psd': str(root / 'PODCAST/學弟請準備底BAR.psd'),
                       'cover_psd': str(root / 'PODCAST/2026 PODCAST新版封面.psd')},
        'output': {'width': 1920, 'height': 1080, 'fps': 60,
                   'video_codec': 'h264', 'video_profile': 'Main',
                   'audio_sample_rate': 44100, 'audio_channels': 2, 'audio_bitrate': 192000,
                   'burn_cc': False, 'embed_cc_stream': False},
        'deliverables': {role: str(media / f'EP{episode}{suffix}') for role, suffix in [
            ('video', '.mp4'), ('audio', '.mp3'), ('cover', '.png'),
            ('youtube_info', '_YT資訊.txt'), ('cc', '.srt')]},
        'acceptance_policy': {'full_word_by_word_listening_optional': False,
                              'source': '公開版預設需完整聽校；僅可按當次使用者明確授權豁免並記錄依據。'},
        'state': 'inventory_only_no_roles_assigned',
    }
    report = {'schema_version': 2, 'episode': episode,
              'checks': [{'id': f'{i:02}', 'criterion': text, 'status': 'pending', 'evidence': ''}
                         for i, text in enumerate(CRITERIA, 1)],
              'waivers': {}, 'artifact_roles': {}, 'artifacts_sha256': {},
              'reviews': {}, 'video_evidence': {},
              'actual_export_semantically_matches_latest_draft': False}
    payloads = {names[0]: config, names[1]: report}
    if rows is not None:
        payloads['media-inventory.json'] = {'media_dir': str(media), 'roles_not_inferred': True,
                                           'files': rows, 'errors': sum('error' in row for row in rows)}
    work.mkdir(parents=True, exist_ok=True)
    for name, payload in payloads.items():
        with (work / name).open('x', encoding='utf-8') as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write('\n')
    return {'episode': episode, 'created': [str(work / name) for name in payloads],
            'probe_errors': sum('error' in row for row in rows) if rows is not None else 0,
            'media_and_draft_modified': False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episode', type=int, required=True)
    parser.add_argument('--media-dir', required=True)
    parser.add_argument('--work-dir', required=True)
    parser.add_argument('--probe', action='store_true')
    parser.add_argument('--ffprobe', default='ffprobe')
    args = parser.parse_args()
    try:
        result = initialize(args.episode, args.media_dir, args.work_dir, args.probe, args.ffprobe)
    except (ValueError, OSError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result['probe_errors'] else 0

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
