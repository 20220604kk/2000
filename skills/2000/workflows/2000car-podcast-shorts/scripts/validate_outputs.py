#!/usr/bin/env python3
"""Validate a directory of rendered 2000CAR podcast shorts."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def command(args):
    return subprocess.run(args, text=True, capture_output=True, encoding="utf-8", errors="replace")


def probe(path):
    result = command([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames",
        "-show_entries", "format=duration", "-of", "json", str(path),
    ])
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    payload = json.loads(result.stdout)
    return payload["format"], payload["streams"][0]


def measure_loudness(path):
    result = command([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-filter_complex", "ebur128=peak=true", "-f", "null", "-",
    ])
    log = result.stderr
    integrated = re.search(r"Integrated loudness:\s+I:\s+(-?[0-9.]+) LUFS", log)
    peak = re.search(r"True peak:\s+Peak:\s+(-?[0-9.]+) dBFS", log)
    return (
        float(integrated.group(1)) if integrated else None,
        float(peak.group(1)) if peak else None,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--duration", type=float, default=13.0)
    parser.add_argument("--fps", type=float, default=60.0)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--loudness", action="store_true")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    files = sorted(args.directory.glob("*.mp4"))
    if not files:
        print(f"No MP4 files found in {args.directory}", file=sys.stderr)
        return 2

    expected_frames = round(args.duration * args.fps)
    failures = 0
    rows = []
    for path in files:
        try:
            fmt, stream = probe(path)
            duration = float(fmt["duration"])
            num, den = (float(item) for item in stream["r_frame_rate"].split("/"))
            fps = num / den
            frames = int(stream["nb_read_frames"])
            decode = command(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"]).returncode == 0
            valid = (
                abs(duration - args.duration) <= 0.01
                and abs(fps - args.fps) <= 0.01
                and frames == expected_frames
                and stream["width"] == args.width
                and stream["height"] == args.height
                and decode
            )
            loudness, peak = measure_loudness(path) if args.loudness else (None, None)
            failures += 0 if valid else 1
            rows.append({
                "file": path.name,
                "duration": duration,
                "frames": frames,
                "fps": fps,
                "size": f"{stream['width']}x{stream['height']}",
                "decode_ok": decode,
                "lufs": loudness,
                "peak_dbfs": peak,
                "valid": valid,
            })
        except Exception as exc:
            failures += 1
            rows.append({"file": path.name, "valid": False, "error": str(exc)})

    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
