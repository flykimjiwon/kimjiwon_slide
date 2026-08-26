#!/usr/bin/env python3
"""sbtifull/ 안의 이미지에서 회사 식별자를 지운다. 원본 assets는 건드리지 않는다.

- MASK: 좌표 박스를 불투명 사각형으로 덮는다 (블러 아님 — 복원 불가).
- EXCLUDE: 회사 식별이 통째로 되는 자료는 중립 플레이스홀더로 교체한다.
좌표는 이미지 크기 대비 비율(0~1). left, top, right, bottom.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sbtifull"

MASK = {
    "sbti2/assets/tweb_admin.png": [
        ((0.000, 0.945, 0.160, 1.000), "계정 정보"),
        ((0.005, 0.683, 0.140, 0.723), "제품명"),
    ],
    "sbti2/assets/tweb_chat.png": [
        ((0.005, 0.005, 0.100, 0.048), "제품명"),
        ((0.005, 0.852, 0.130, 0.894), "제품명"),
        ((0.000, 0.950, 0.160, 1.000), "계정 정보"),
        ((0.480, 0.978, 0.680, 1.000), "제품명"),
    ],
    # build_sbtifull.py의 ASSET_RENAME 이후 이름 기준 (tgc_* -> aict_*)
    "sbti3/assets/aict_wiki_mcp_ask.png": [
        ((0.020, 0.004, 0.300, 0.032), "제품명"),
        ((0.020, 0.040, 0.365, 0.072), "내부 문서명"),
        ((0.335, 0.448, 0.675, 0.479), "제품명"),
        ((0.030, 0.853, 0.755, 0.892), "실명"),
    ],
    "sbti3/assets/aict_devreq_aicr.png": [
        ((0.213, 0.020, 0.292, 0.074), "회사 로고"),
        ((0.748, 0.423, 0.847, 0.480), "부서명"),
        ((0.006, 0.116, 0.187, 0.180), "제품명"),
        ((0.193, 0.793, 0.342, 0.840), "실명"),
    ],
    # ── 2026-08-26 증분: openclaw 캡처의 개인 텔레그램 정보 ──
    # 상단 타이틀바에 개인 계정 핸들("Telegram @ ..."), 본문·상태줄에 오너 chatId
    "sbti1/assets/openclaw_tg_carfilter.png": [
        ((0.000, 0.000, 1.000, 0.042), "계정 정보"),
    ],
    "sbti1/assets/openclaw_tg_hotel.png": [
        ((0.000, 0.000, 1.000, 0.042), "계정 정보"),
    ],
    "sbti1/assets/openclaw_tg_test.png": [
        ((0.000, 0.000, 1.000, 0.042), "계정 정보"),
    ],
    "sbti1/assets/openclaw_tui.png": [
        ((0.000, 0.000, 1.000, 0.040), "로컬 경로"),
        ((0.255, 0.405, 0.535, 0.480), "개인 ID"),
        ((0.325, 0.540, 0.640, 0.610), "개인 ID"),
    ],
    "sbti1/assets/openclaw_webui.png": [
        ((0.000, 0.260, 0.165, 0.302), "개인 ID"),
        ((0.293, 0.390, 0.398, 0.432), "개인 ID"),
    ],
}

EXCLUDE = {
    "sbti2/assets/aicoding_website_landing.png": "사내 포털 화면 · 공개본 제외",
    "sbti3/assets/ttaengyo_logo.png":          "제휴 서비스 로고 · 공개본 제외",
    "sbti3/assets/ttaeng_poc_poster.jpg":      "PoC 시연 영상 · 공개본 제외",
}
EXCLUDE_VIDEO = ["sbti3/assets/ttaeng_poc_captioned.mp4"]

# 영상을 지우면 <video>가 깨진 참조로 남는다. 안내 블록으로 갈아끼운다.
VIDEO_SWAP = [(
    "sbti3/index.html",
    '<video src="assets/ttaeng_poc_captioned.mp4" poster="assets/ttaeng_poc_poster.jpg"'
    ' controls preload="metadata"></video>',
    '<div style="display:grid;place-items:center;gap:10px;width:100%;aspect-ratio:16/9;'
    'background:#171e2c;border:1px solid #475569;border-radius:14px;color:#94a3b8;'
    'font-size:17px;font-weight:700;letter-spacing:.01em">'
    '<span style="font-size:30px;opacity:.5">▣</span>'
    'PoC 시연 영상 · 공개본 제외'
    '<span style="font-size:13px;font-weight:400;opacity:.75">'
    '실제 서비스 화면이 담겨 있어 외부 공개본에서는 제외했습니다</span></div>'
)]

FONTS = ["/System/Library/Fonts/AppleSDGothicNeo.ttc",
         "/System/Library/Fonts/Supplemental/AppleGothic.ttf"]


def font(size):
    for f in FONTS:
        try:
            return ImageFont.truetype(f, size)
        except Exception:
            continue
    return ImageFont.load_default()


def do_mask():
    for rel, boxes in MASK.items():
        p = OUT / rel
        im = Image.open(p).convert("RGB")
        W, H = im.size
        d = ImageDraw.Draw(im)
        for (l, t, r, b), label in boxes:
            box = (int(l*W), int(t*H), int(r*W), int(b*H))
            d.rectangle(box, fill=(31, 41, 55))
            h = box[3] - box[1]
            fs = max(9, min(int(h * 0.5), 34))
            d.text((box[0] + 8, box[1] + (h - fs) / 2 - 2),
                   "● 비공개", fill=(148, 163, 184), font=font(fs))
        im.save(p)
        print(f"MASK    {rel}  {len(boxes)}박스")


def do_exclude():
    for rel, msg in EXCLUDE.items():
        p = OUT / rel
        W, H = Image.open(p).size
        im = Image.new("RGB", (W, H), (23, 30, 44))
        d = ImageDraw.Draw(im)
        d.rectangle((6, 6, W-7, H-7), outline=(71, 85, 105), width=max(2, W//500))
        fs = max(12, min(W // 26, 44))
        f = font(fs)
        tb = d.textbbox((0, 0), msg, font=f)
        d.text(((W-(tb[2]-tb[0]))/2, (H-(tb[3]-tb[1]))/2), msg,
               fill=(148, 163, 184), font=f)
        im.save(p)
        print(f"EXCLUDE {rel}  ({W}x{H})")
    for rel in EXCLUDE_VIDEO:
        p = OUT / rel
        if p.exists():
            p.unlink()
            print(f"EXCLUDE {rel}  (삭제)")


def do_video_swap():
    for rel, old, new in VIDEO_SWAP:
        p = OUT / rel
        s = p.read_text(encoding="utf-8")
        if old not in s:
            print(f"SWAP    {rel}  ! 대상 마크업 없음 — 확인 필요")
            continue
        p.write_text(s.replace(old, new), encoding="utf-8")
        print(f"SWAP    {rel}  <video> -> 안내 블록")


if __name__ == "__main__":
    do_mask()
    do_exclude()
    do_video_swap()
    sys.exit(0)
