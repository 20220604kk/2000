"""Check a completed 2000reels local ledger; this does not query websites."""
import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

PLATFORMS = ("tiktok", "youtube", "facebook", "instagram")


def check(data):
    errors = []
    items = data.get("items", [])
    if data.get("timezone") != "Asia/Taipei":
        errors.append("timezone must be Asia/Taipei")
    if data.get("expectedVideos") != len(items) or not items:
        errors.append("expectedVideos does not match a nonempty items list")
    expected = len(items) * len(PLATFORMS)
    if data.get("expectedPlatformTasks") != expected:
        errors.append("expectedPlatformTasks must include all four endpoints")
    slots, sources = set(), set()
    completed = 0
    for index, item in enumerate(items, 1):
        label = f"item {index} ({item.get('name', '?')})"
        title = item.get("title", "")
        if not (title.startswith("《") and title.endswith("》") and 0 < len(title[1:-1]) <= 13):
            errors.append(f"{label}: title format/length")
        source = item.get("source")
        if not source or source in sources:
            errors.append(f"{label}: missing or duplicate source")
        sources.add(source)
        stamp = item.get("scheduledAt")
        try:
            dt = datetime.fromisoformat(stamp)
            if dt.utcoffset() != timedelta(hours=8) or dt.hour not in (18, 20) or dt.minute or dt.second:
                errors.append(f"{label}: invalid Taipei publication slot")
            if dt.weekday() == 5 and dt.hour == 20:
                errors.append(f"{label}: Saturday 20:00 must be skipped")
            if dt in slots:
                errors.append(f"{label}: duplicate publication slot")
            slots.add(dt)
        except (TypeError, ValueError):
            errors.append(f"{label}: invalid scheduledAt")
        for platform in PLATFORMS:
            state = item.get("platforms", {}).get(platform, {})
            if state.get("state") != "scheduled":
                errors.append(f"{label}/{platform}: not verified scheduled")
            else:
                completed += 1
            if state.get("title") != title or state.get("scheduledAt") != stamp:
                errors.append(f"{label}/{platform}: canonical title/time mismatch")
            if platform != "tiktok" and state.get("localCoverUploaded") is not True:
                errors.append(f"{label}/{platform}: local cover not recorded")
            if not (state.get("url") or state.get("managementUrl")):
                errors.append(f"{label}/{platform}: missing result/management URL")
            if not state.get("verification"):
                errors.append(f"{label}/{platform}: missing website verification record")
    if data.get("completedPlatformTasks") != completed:
        errors.append("completedPlatformTasks does not match recorded states")
    return errors, completed, expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    errors, completed, expected = check(data)
    print(json.dumps({"ok": not errors, "completed": completed, "expected": expected, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
