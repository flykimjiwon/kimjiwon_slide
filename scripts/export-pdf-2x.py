#!/usr/bin/env python3
"""Export the make-slide HTML deck to a high-quality 2x screenshot PDF.

Creates one temporary HTML per slide, captures it with Chrome at 1920x1080
with device scale factor 2, then combines the 3840x2160 PNGs into a 16:9 PDF.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PyMuPDF(fitz) is required: {exc}")

ROOT = Path(__file__).resolve().parents[1]
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SLIDE_RE = re.compile(r'<section class="slide[^\"]*"[^>]*>.*?</section>', re.S)

EXPORT_CSS = """
<style id="pdf-export-css">
  .progress,.counter,.hint,.controls,.notes{display:none!important}
  .slide{opacity:0!important;pointer-events:none!important;transition:none!important}
  .slide[data-export-active="true"]{opacity:1!important;pointer-events:auto!important}
  .slide[data-export-active="true"] video{pointer-events:none!important}
</style>
"""

VIDEO_SCRIPT = """
<script id="pdf-export-video-script">
  document.addEventListener('DOMContentLoaded', () => {
    for (const v of document.querySelectorAll('video')) {
      v.controls = false;
      v.muted = true;
      v.preload = 'metadata';
      try { v.currentTime = 1.0; } catch (e) {}
      try { v.pause(); } catch (e) {}
    }
  });
</script>
"""


def make_export_html(source: str, slide_index: int) -> str:
    def mark(match: re.Match, count=[0]):
        count[0] += 1
        section = match.group(0)
        section = re.sub(r'\sactive(?=[" ])', '', section, count=1)
        if count[0] == slide_index:
            section = section.replace('<section ', '<section data-export-active="true" ', 1)
        return section

    html = SLIDE_RE.sub(mark, source)
    html = html.replace('<head>', f'<head><base href="{ROOT.as_uri()}/">', 1)
    html = html.replace('</style>', '</style>' + EXPORT_CSS, 1)
    html = html.replace('</body>', VIDEO_SCRIPT + '</body>', 1)
    return html


def chrome_capture(html_path: Path, png_path: Path, scale: int, width: int, height: int) -> None:
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        "--allow-file-access-from-files",
        f"--window-size={width},{height}",
        f"--force-device-scale-factor={scale}",
        "--virtual-time-budget=2500",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_pdf(pngs: list[Path], output: Path, width: int, height: int) -> None:
    doc = fitz.open()
    rect = fitz.Rect(0, 0, width, height)
    for png in pngs:
        page = doc.new_page(width=width, height=height)
        page.insert_image(rect, filename=str(png), keep_proportion=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output), deflate=True, garbage=4)
    doc.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='index.html')
    ap.add_argument('--output', default='assets/techaicode_final_slide.pdf')
    ap.add_argument('--width', type=int, default=1920)
    ap.add_argument('--height', type=int, default=1080)
    ap.add_argument('--scale', type=int, default=2)
    ap.add_argument('--keep-workdir', action='store_true')
    args = ap.parse_args()

    if not CHROME.exists():
        raise SystemExit(f"Chrome not found: {CHROME}")

    source_path = ROOT / args.input
    output_path = ROOT / args.output
    source = source_path.read_text(encoding='utf-8')
    slides = SLIDE_RE.findall(source)
    if not slides:
        raise SystemExit('No slides found')

    workdir = Path(tempfile.mkdtemp(prefix='techaicode-pdf-2x-'))
    pngs: list[Path] = []
    try:
        for i in range(1, len(slides) + 1):
            html = make_export_html(source, i)
            html_path = workdir / f'slide-{i:02d}.html'
            png_path = workdir / f'slide-{i:02d}.png'
            html_path.write_text(html, encoding='utf-8')
            chrome_capture(html_path, png_path, args.scale, args.width, args.height)
            pngs.append(png_path)
            print(f'captured {i:02d}/{len(slides)} {png_path.name}', flush=True)
        build_pdf(pngs, output_path, args.width, args.height)
        print(f'wrote {output_path.relative_to(ROOT)}', flush=True)
        print(f'pages {len(slides)}', flush=True)
        print(f'workdir {workdir}', flush=True)
    finally:
        if not args.keep_workdir:
            shutil.rmtree(workdir, ignore_errors=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
