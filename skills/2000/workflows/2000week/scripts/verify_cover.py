"""Check the saved native PSD and exported PNG; create a QA thumbnail."""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('template', 'psd', 'png', 'title', 'date'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--psd-tools-dir')
    args = parser.parse_args()
    if args.psd_tools_dir:
        sys.path.insert(0, args.psd_tools_dir)
    from PIL import Image, ImageChops, ImageStat
    from psd_tools import PSDImage

    native = PSDImage.open(args.psd)
    source = PSDImage.open(args.template)
    image = Image.open(args.png).convert('RGB')
    assert native.size == source.size == image.size, 'PSD/PNG/template dimensions differ'
    visible_types = [layer for layer in native.descendants() if layer.kind == 'type' and layer.is_visible()]
    texts = [layer.text for layer in visible_types]
    assert args.title in texts, 'Editable current title is missing'
    assert args.date in texts, 'Editable current date is missing'
    assert 'MG ZS' not in texts or args.title == 'MG ZS', 'Old visible headline remains'
    assert '20260930' not in texts or args.date == '20260930', 'Old visible date remains'
    assert '兩千の直播夜車' in texts, 'Show name was lost'
    preview = native.topil().convert('RGB')
    stats = ImageStat.Stat(ImageChops.difference(preview, image))
    mean_error = sum(stats.mean) / 3
    assert mean_error < 1.0, f'PSD merged preview differs from PNG: {mean_error}'
    output = Path(args.png)
    prior_report = output.parent / (args.date + '_封面檢查.json')
    if prior_report.exists():
        prior = json.loads(prior_report.read_text(encoding='utf-8-sig'))
        assert digest(args.template).lower() == prior['templateSha256'].lower(), 'Template changed'
    thumb = output.with_name(output.stem + '_320x180.jpg')
    image.resize((320, 180), Image.Resampling.LANCZOS).save(thumb, quality=95)
    report = {
        'title': args.title, 'date': args.date, 'dimensions': list(image.size),
        'native_title_and_date': True, 'visible_texts': texts,
        'psd_png_mean_error': mean_error, 'thumbnail': str(thumb.resolve()),
        'files': {str(Path(p).resolve()): {'bytes': Path(p).stat().st_size, 'sha256': digest(p)}
                  for p in (args.template, args.psd, args.png)},
        'visual_review': 'Inspect the original-size PNG and thumbnail separately.'
    }
    target = output.parent / (args.date + '_檔案驗證.json')
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'passed': True, 'report': str(target), 'mean_error': mean_error}, ensure_ascii=True))


if __name__ == '__main__':
    main()
