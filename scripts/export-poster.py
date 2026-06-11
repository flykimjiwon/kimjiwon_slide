#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
CHROME = Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
PAGE_RE = re.compile(r'<section class="poster-page[^"]*"[^>]*>.*?</section>', re.S)
EXPORT_CSS = """
<style id="poster-export-css">
  body{background:#fff!important;margin:0!important;overflow:hidden!important}
  .deck{display:block!important;padding:0!important}
  .poster-page{position:absolute!important;left:0!important;top:0!important;box-shadow:none!important;border-radius:0!important;display:none!important}
  .poster-page[data-export-active="true"]{display:block!important}
</style>
"""

def make_page_html(source: str, index: int) -> str:
    def mark(match: re.Match, count=[0]):
        count[0] += 1
        section = match.group(0)
        if count[0] == index:
            section = section.replace('<section ', '<section data-export-active="true" ', 1)
        return section
    html = PAGE_RE.sub(mark, source)
    html = html.replace('<head>', f'<head><base href="{ROOT.as_uri()}/">', 1)
    html = html.replace('</style>', '</style>' + EXPORT_CSS, 1)
    return html

def chrome_capture(html_path: Path, png_path: Path, scale: int, width: int, height: int) -> None:
    cmd = [
        str(CHROME), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
        '--no-default-browser-check', '--allow-file-access-from-files', f'--window-size={width},{height}',
        f'--force-device-scale-factor={scale}', '--virtual-time-budget=2500', f'--screenshot={png_path}', html_path.as_uri()
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def build_pdf(pngs: list[Path], output: Path, width: int, height: int) -> None:
    doc = fitz.open(); rect = fitz.Rect(0,0,width,height)
    for png in pngs:
        page = doc.new_page(width=width, height=height)
        page.insert_image(rect, filename=str(png), keep_proportion=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output), deflate=True, garbage=4)
    doc.close()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='poster.html')
    ap.add_argument('--output-pdf', default='assets/techaicode_poster.pdf')
    ap.add_argument('--output-prefix', default='assets/techaicode_poster_page')
    ap.add_argument('--width', type=int, default=1080)
    ap.add_argument('--height', type=int, default=1920)
    ap.add_argument('--scale', type=int, default=2)
    ap.add_argument('--keep-workdir', action='store_true')
    args = ap.parse_args()
    if not CHROME.exists():
        raise SystemExit(f'Chrome not found: {CHROME}')
    source = (ROOT / args.input).read_text(encoding='utf-8')
    pages = PAGE_RE.findall(source)
    if not pages:
        raise SystemExit('No poster pages found')
    workdir = Path(tempfile.mkdtemp(prefix='techaicode-poster-'))
    exported: list[Path] = []
    try:
        for i in range(1, len(pages)+1):
            html_path = workdir / f'poster-{i:02d}.html'
            tmp_png = workdir / f'poster-{i:02d}.png'
            final_png = ROOT / f'{args.output_prefix}_{i:02d}.png'
            html_path.write_text(make_page_html(source, i), encoding='utf-8')
            chrome_capture(html_path, tmp_png, args.scale, args.width, args.height)
            final_png.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(tmp_png, final_png)
            exported.append(final_png)
            print(f'captured {i:02d}/{len(pages)} {final_png.relative_to(ROOT)}', flush=True)
        build_pdf(exported, ROOT / args.output_pdf, args.width, args.height)
        print(f'wrote {args.output_pdf}', flush=True)
        print(f'pages {len(pages)}', flush=True)
        print(f'workdir {workdir}', flush=True)
    finally:
        if not args.keep_workdir:
            shutil.rmtree(workdir, ignore_errors=True)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
