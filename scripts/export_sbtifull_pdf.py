#!/usr/bin/env python3
"""sbtifull 모자이크 3부작(sbti1~3 사본)을 한 권의 공개용 PDF로 내보낸다.

원본 PDF(assets/sbti{n}.pdf)는 마스킹 이전이라 공개본에서 제외된 물건이다.
이 스크립트는 **마스킹 완료된 sbtifull/ 사본만** 읽어 공개 가능한 PDF를 만든다.
원본 sbti1~3/ 은 읽지 않는다. 반드시 build → redact 가 끝난 상태에서 돌릴 것.

출력: sbtifull/SBTI_공개본.pdf (뷰어 1페이지의 다운로드 버튼이 이 이름을 참조)

usage: python3 scripts/export_sbtifull_pdf.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pdf_image_processing import build_pdf

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sbtifull"
OUT_PDF = SRC / "SBTI_공개본.pdf"
DECKS = ["sbti1", "sbti2", "sbti3"]
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SLIDE_RE = re.compile(r'<section class="slide[^"]*"[^>]*>.*?</section>', re.S)
WIDTH, HEIGHT, SCALE = 1920, 1080, 2

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


def make_export_html(source: str, deck: str, slide_index: int) -> str:
    def mark(match: re.Match, count: list = [0]) -> str:
        count[0] += 1
        section = match.group(0)
        section = re.sub(r'\sactive(?=[" ])', '', section, count=1)
        if count[0] == slide_index:
            section = section.replace('<section ', '<section data-export-active="true" ', 1)
        return section

    html = SLIDE_RE.sub(mark, source)
    # 임시 HTML은 workdir에 쓰이므로 base를 사본 덱 폴더의 file:// 로 돌려놓는다.
    deck_uri = (SRC / deck).resolve().as_uri()
    old_base = f'<base href="/sbtifull/{deck}/">'
    if old_base not in html:
        raise SystemExit(f"[{deck}] {old_base} 를 찾지 못함 — 사본 head 구조 확인 필요")
    html = html.replace(old_base, f'<base href="{deck_uri}/">')
    # file: 폴백이 base를 ./(=workdir)로 되돌려 에셋이 깨지는 것 차단
    html = re.sub(r'<script>if\(location\.protocol==="file:"\)\{.*?</script>',
                  '', html, flags=re.S)
    html = html.replace('</style>', '</style>' + EXPORT_CSS, 1)
    html = html.replace('</body>', VIDEO_SCRIPT + '</body>', 1)
    return html


def chrome_capture(html_path: Path, png_path: Path) -> None:
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        "--allow-file-access-from-files",
        f"--window-size={WIDTH},{HEIGHT}",
        f"--force-device-scale-factor={SCALE}",
        "--virtual-time-budget=2500",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> int:
    if not CHROME.exists():
        raise SystemExit(f"Chrome not found: {CHROME}")

    # 사본이 공개본인지 표식으로 재확인 — 원본을 실수로 찍는 사고 방지
    for deck in DECKS:
        head = (SRC / deck / "index.html").read_text(encoding="utf-8")[:2000]
        if 'x-sbti-build" content="mosaic' not in head:
            raise SystemExit(f"[{deck}] mosaic 표식 없음 — build_sbtifull.py 부터 다시")

    workdir = Path(tempfile.mkdtemp(prefix="sbtifull-pdf-"))
    pngs: list[Path] = []
    page = 0
    try:
        for deck in DECKS:
            source = (SRC / deck / "index.html").read_text(encoding="utf-8")
            n = len(SLIDE_RE.findall(source))
            for idx in range(1, n + 1):
                page += 1
                html_path = workdir / f"p{page:03d}.html"
                png_path = workdir / f"p{page:03d}.png"
                html_path.write_text(make_export_html(source, deck, idx), encoding="utf-8")
                chrome_capture(html_path, png_path)
                pngs.append(png_path)
                print(f"captured {page:03d} ({deck} {idx}/{n})", flush=True)
        build_pdf(pngs, OUT_PDF, WIDTH, HEIGHT, 1.0,
                  pdf_image_format="jpeg", jpeg_quality=92)
        size_mb = OUT_PDF.stat().st_size / 1e6
        print(f"wrote {OUT_PDF.relative_to(ROOT)} · {page}p · {size_mb:.1f}MB", flush=True)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
