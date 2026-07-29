#!/usr/bin/env python3
"""Export the make-slide HTML deck to a high-quality 2x screenshot PDF.

Creates one temporary HTML per slide, captures it with Chrome at 1920x1080
with device scale factor 2, then combines the 3840x2160 PNGs into a 16:9 PDF.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from pdf_image_processing import build_pdf

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


def make_export_html(source: str, slide_index: int, source_dir: Path) -> str:
    def mark(match: re.Match[str], count: list[int] = [0]) -> str:
        count[0] += 1
        section = match.group(0)
        section = re.sub(r'\sactive(?=[" ])', '', section, count=1)
        if count[0] == slide_index:
            section = section.replace('<section ', '<section data-export-active="true" ', 1)
        return section

    html = SLIDE_RE.sub(mark, source)
    html = html.replace('<head>', f'<head><base href="{source_dir.resolve().as_uri()}/">', 1)
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='index.html')
    ap.add_argument('--output', default='assets/techaicode_final_slide.pdf')
    ap.add_argument('--width', type=int, default=1920)
    ap.add_argument('--height', type=int, default=1080)
    ap.add_argument('--scale', type=int, default=2)
    ap.add_argument(
        '--pdf-image-format',
        choices=('png', 'jpeg'),
        default='jpeg',
        help='Image format embedded into the final PDF. JPEG q95 keeps the deck under 10MB with minimal visible quality loss.',
    )
    ap.add_argument('--jpeg-quality', type=int, default=95)
    ap.add_argument(
        '--zoom-after-first',
        type=float,
        default=1.0,
        help='Target content-safe zoom for PDF pages after page 1. Example: 1.3 keeps page 1 unchanged and crops whitespace on pages 2+ up to 30%% without cutting detected content.',
    )
    ap.add_argument(
        '--no-zoom-pages',
        default='',
        help='Comma-separated page numbers to keep unzoomed even when --zoom-after-first is set. Example: 4,6',
    )
    ap.add_argument('--keep-workdir', action='store_true')
    args = ap.parse_args()
    no_zoom_pages = {
        int(page.strip())
        for page in args.no_zoom_pages.split(',')
        if page.strip()
    }

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
            html = make_export_html(source, i, source_path.parent)
            html_path = workdir / f'slide-{i:02d}.html'
            png_path = workdir / f'slide-{i:02d}.png'
            html_path.write_text(html, encoding='utf-8')
            chrome_capture(html_path, png_path, args.scale, args.width, args.height)
            pngs.append(png_path)
            print(f'captured {i:02d}/{len(slides)} {png_path.name}', flush=True)
        build_pdf(
            pngs,
            output_path,
            args.width,
            args.height,
            args.zoom_after_first,
            no_zoom_pages=no_zoom_pages,
            pdf_image_format=args.pdf_image_format,
            jpeg_quality=args.jpeg_quality,
        )
        print(f'wrote {output_path.relative_to(ROOT)}', flush=True)
        print(f'pages {len(slides)}', flush=True)
        print(f'pdf_image_format {args.pdf_image_format}', flush=True)
        if args.pdf_image_format == 'jpeg':
            print(f'jpeg_quality {args.jpeg_quality}', flush=True)
        print(f'zoom_after_first {args.zoom_after_first}', flush=True)
        if no_zoom_pages:
            print(f'no_zoom_pages {",".join(map(str, sorted(no_zoom_pages)))}', flush=True)
        print(f'workdir {workdir}', flush=True)
    finally:
        if not args.keep_workdir:
            shutil.rmtree(workdir, ignore_errors=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
