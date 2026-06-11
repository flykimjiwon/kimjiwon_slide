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

try:
    from PIL import Image, ImageFilter
except Exception:  # pragma: no cover
    Image = None
    ImageFilter = None

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


def detail_bbox(png: Path) -> tuple[int, int, int, int] | None:
    """Return a rough detail bounding box so zoom crops whitespace, not content."""
    if Image is None or ImageFilter is None:
        return None
    with Image.open(png) as raw:
        gray = raw.convert("L")
        # FIND_EDGES ignores smooth slide backgrounds but catches text, cards,
        # screenshots, video frames, and chart boundaries.
        edges = gray.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(9))
        mask = edges.point(lambda p: 255 if p > 70 else 0)
        # Pillow's edge filter treats the outer image boundary as a strong edge.
        # Zero a thin border so slide-canvas edges do not prevent whitespace crop.
        border = 64
        width, height = mask.size
        pixels = mask.load()
        for x in range(width):
            for y in range(border):
                pixels[x, y] = 0
                pixels[x, height - 1 - y] = 0
        for y in range(height):
            for x in range(border):
                pixels[x, y] = 0
                pixels[width - 1 - x, y] = 0
        # Some slides have large, low-opacity section numbers like 01 / 02 in
        # the top-left corner. They are decorative and should not pull the PDF
        # zoom crop away from the actual slide content.
        decorative_w = min(width, 620)
        decorative_h = min(height, 470)
        for x in range(decorative_w):
            for y in range(decorative_h):
                pixels[x, y] = 0
        return mask.getbbox()


def crop_for_zoom(png: Path, output: Path, target_zoom: float) -> tuple[Path, float]:
    """Crop around detected content with up to target_zoom, preserving 16:9."""
    if target_zoom <= 1.0 or Image is None:
        return png, 1.0

    with Image.open(png) as raw:
        image = raw.convert("RGB")
        width, height = image.size
        bbox = detail_bbox(png)
        if not bbox:
            bbox = (0, 0, width, height)

        # Add a visual safety margin around detected details. Screenshots are 2x,
        # so 140px here is about 70 CSS px in the slide.
        margin = 140
        x0 = max(0, bbox[0] - margin)
        y0 = max(0, bbox[1] - margin)
        x1 = min(width, bbox[2] + margin)
        y1 = min(height, bbox[3] + margin)
        bbox_w = max(1, x1 - x0)
        bbox_h = max(1, y1 - y0)

        aspect = width / height
        target_w = width / target_zoom
        target_h = height / target_zoom

        crop_w = max(target_w, bbox_w)
        crop_h = crop_w / aspect
        if crop_h < bbox_h:
            crop_h = bbox_h
            crop_w = crop_h * aspect

        crop_w = min(width, crop_w)
        crop_h = min(height, crop_h)

        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        left = min(max(0, cx - crop_w / 2), width - crop_w)
        top = min(max(0, cy - crop_h / 2), height - crop_h)
        right = left + crop_w
        bottom = top + crop_h

        crop = image.crop((round(left), round(top), round(right), round(bottom)))
        crop.save(output)
        effective_zoom = width / (right - left)
        return output, effective_zoom


def build_pdf(
    pngs: list[Path],
    output: Path,
    width: int,
    height: int,
    zoom_after_first: float = 1.0,
    no_zoom_pages: set[int] | None = None,
) -> None:
    doc = fitz.open()
    rect = fitz.Rect(0, 0, width, height)
    crop_dir = output.parent / ".pdf-export-crops"
    effective_zooms: list[float] = []
    no_zoom_pages = no_zoom_pages or set()
    for index, png in enumerate(pngs, start=1):
        page = doc.new_page(width=width, height=height)
        pdf_png = png
        effective_zoom = 1.0
        if index > 1 and index not in no_zoom_pages and zoom_after_first > 1.0:
            crop_dir.mkdir(parents=True, exist_ok=True)
            pdf_png, effective_zoom = crop_for_zoom(
                png,
                crop_dir / f"slide-{index:02d}-zoom.png",
                zoom_after_first,
            )
        effective_zooms.append(effective_zoom)
        page.insert_image(rect, filename=str(pdf_png), keep_proportion=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output), deflate=True, garbage=4)
    doc.close()
    if crop_dir.exists():
        shutil.rmtree(crop_dir, ignore_errors=True)
    if zoom_after_first > 1.0:
        zoom_text = ", ".join(f"{z:.2f}" for z in effective_zooms)
        print(f"effective_zooms {zoom_text}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='index.html')
    ap.add_argument('--output', default='assets/techaicode_final_slide.pdf')
    ap.add_argument('--width', type=int, default=1920)
    ap.add_argument('--height', type=int, default=1080)
    ap.add_argument('--scale', type=int, default=2)
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
            html = make_export_html(source, i)
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
        )
        print(f'wrote {output_path.relative_to(ROOT)}', flush=True)
        print(f'pages {len(slides)}', flush=True)
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
