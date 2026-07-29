"""Crop slide captures and assemble them into a compact PDF."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Literal, assert_never

try:
    import fitz  # PyMuPDF
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"PyMuPDF(fitz) is required: {exc}") from exc

try:
    from PIL import Image, ImageFilter
except ImportError:  # pragma: no cover
    Image = None
    ImageFilter = None

type PdfImageFormat = Literal["png", "jpeg"]


def detail_bbox(png: Path) -> tuple[int, int, int, int] | None:
    """Return a rough detail bounding box so zoom crops whitespace, not content."""
    if Image is None or ImageFilter is None:
        return None
    with Image.open(png) as raw:
        gray = raw.convert("L")
        # FIND_EDGES ignores smooth slide backgrounds but catches text, cards,
        # screenshots, video frames, and chart boundaries.
        edges = gray.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(9))
        mask = edges.point([0] * 71 + [255] * 185)
        # Pillow's edge filter treats the outer image boundary as a strong edge.
        # Zero a thin border so slide-canvas edges do not prevent whitespace crop.
        border = 64
        width, height = mask.size
        pixels = mask.load()
        assert pixels is not None
        for x in range(width):
            for y in range(border):
                pixels[x, y] = 0
                pixels[x, height - 1 - y] = 0
        for y in range(height):
            for x in range(border):
                pixels[x, y] = 0
                pixels[width - 1 - x, y] = 0
        # Decorative section numbers in the top-left should not pull the crop
        # away from the actual slide content.
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

        # Screenshots are 2x, so 140px is about 70 CSS px in the slide.
        margin = 140
        x0 = max(0, bbox[0] - margin)
        y0 = max(0, bbox[1] - margin)
        x1 = min(width, bbox[2] + margin)
        y1 = min(height, bbox[3] + margin)
        bbox_w = max(1, x1 - x0)
        bbox_h = max(1, y1 - y0)

        aspect = width / height
        target_w = width / target_zoom
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
        return output, width / (right - left)


def prepare_pdf_image(
    source: Path,
    output: Path,
    image_format: PdfImageFormat,
    jpeg_quality: int,
) -> Path:
    """Prepare an image file for embedding in the PDF."""
    match image_format:
        case "png":
            return source
        case "jpeg":
            if Image is None:
                raise SystemExit("Pillow is required for JPEG PDF export")
        case _ as unreachable:
            assert_never(unreachable)

    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as raw:
        raw.convert("RGB").save(
            output,
            "JPEG",
            quality=jpeg_quality,
            optimize=True,
            progressive=True,
            # Keep 4:4:4 chroma sampling so small UI text stays crisp.
            subsampling=0,
        )
    return output


def build_pdf(
    pngs: list[Path],
    output: Path,
    width: int,
    height: int,
    zoom_after_first: float = 1.0,
    no_zoom_pages: set[int] | None = None,
    pdf_image_format: PdfImageFormat = "jpeg",
    jpeg_quality: int = 95,
) -> None:
    """Build a 16:9 PDF from captured slide images."""
    crop_dir = output.parent / ".pdf-export-crops"
    effective_zooms: list[float] = []
    no_zoom_pages = no_zoom_pages or set()
    with fitz.open() as doc:
        rect = fitz.Rect(0, 0, width, height)
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
            extension = "jpg" if pdf_image_format == "jpeg" else "png"
            pdf_image = prepare_pdf_image(
                pdf_png,
                crop_dir / f"slide-{index:02d}.{extension}",
                pdf_image_format,
                jpeg_quality,
            )
            effective_zooms.append(effective_zoom)
            page.insert_image(rect, filename=str(pdf_image), keep_proportion=False)
        output.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(output), deflate=True, garbage=4)

    if crop_dir.exists():
        shutil.rmtree(crop_dir, ignore_errors=True)
    if zoom_after_first > 1.0:
        zoom_text = ", ".join(f"{zoom:.2f}" for zoom in effective_zooms)
        print(f"effective_zooms {zoom_text}", flush=True)
