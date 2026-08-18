#!/usr/bin/env python3
"""sbti1/2/3 원본 -> sbtifull 모자이크본 생성.

원본(sbti1/, sbti2/, sbti3/)은 절대 수정하지 않는다. 읽기만 한다.
CSS blur는 소스에 원문이 남으므로 모자이크로 치지 않는다.
이 스크립트는 문자열 자체를 치환하고 blur 필터를 걷어낸다.

usage: python3 scripts/build_sbtifull.py
"""
import re, shutil, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sbtifull"
DECKS = ["sbti1", "sbti2", "sbti3"]

# ── 1. 실명 22명 → 익명 ────────────────────────────────────────────
NAMES = ["안우일","나창현","이정우","변은서","이광빈","이강희","김윤지","김예진",
         "이상헌","김지은","정다윤","윤정한","서문교","이현지","노태경","박은수",
         "조범석","김혜민","김장원","이승민"]
NAME_MAP = {n: f"참여자 {chr(ord('A')+i)}" for i, n in enumerate(NAMES)}

# ── 2. 부서 실명 → 익명 (긴 것부터) ───────────────────────────────
DEPT_MAP = {
    "AX·디지털솔루션부": "솔루션 개발부",
    "AX 디지털솔루션부": "솔루션 개발부",
    "AX디지털솔루션":   "솔루션 개발",
    "디지털서비스개발부": "서비스 개발 1부",
    "디지털서비스개발":   "서비스 개발 1",
    "정보서비스개발부":   "서비스 개발 2부",
    "정보서비스개발":     "서비스 개발 2",
    "글로벌서비스개발부": "서비스 개발 3부",
    "글로벌서비스개발":   "서비스 개발 3",
    "투자서비스개발부":   "서비스 개발 4부",
    "투자서비스개발":     "서비스 개발 4",
    "금융서비스개발부":   "서비스 개발 5부",
    "여신서비스개발부":   "서비스 개발 6부",
    "기관·제휴개발부":    "제휴 개발부",
    "투자자산수탁부":     "수탁 업무부",
    "신탁솔루션":         "신탁 솔루션",
    "고객마케팅부":       "마케팅부",
    "Data플랫폼Unit":     "데이터 플랫폼 조직",
    "Data플랫폼":         "데이터 플랫폼",
    "땡겨요사업단":       "자체 플랫폼 사업단",
    "ICT아웃소싱(베트남)": "해외 개발 파트너",
    "Tech운영부":         "기술 운영부",
    "Tech기획":           "기술 기획",
    "DS개발팀":           "DS 개발팀",
    "AI개발부":           "AI 개발부",
    "AI개발":             "AI 개발",
    "혁신기술":           "기술 연구",
    "변화추진":           "변화 관리",
    "플랫폼운영":         "플랫폼 운영",
    "CXM":                "채널",
    "기반 AX":            "기반 기술",
}

# ── 3. 회사·조직·내부 시스템 (긴 것부터) ─────────────────────────
ORG_MAP = {
    "신한은행 TECH혁신UNIT 개발 AX CELL 김지원프로": "금융권 A사 · AI 개발 조직 · 김지원",
    "신한은행(외부개발팀)": "외부 개발 파트너",
    "신한은행":       "금융권 A사",
    "TECH혁신UNIT":  "기술혁신 조직",
    "AX CELL":       "AX 조직",
    "은행 내부 개발망": "사내 폐쇄 개발망",
    "은행 내부망":    "사내 폐쇄망",
    "폐쇄망인 은행":  "폐쇄망인 사내",
    "은행 내에":      "사내에",
    "은행의 GITSOP": "사내 형상관리 시스템",
    "GITSOP":        "사내 형상관리 시스템",
    "은행에서의 혁신": "현업에서의 혁신",
    "은행 개발 업무": "사내 개발 업무",
    "사내 스윙 SSO":  "사내 SSO",
    "스윙 SSO":       "사내 SSO",
    "행내":          "사내",
    "사번 기반":      "사내 계정 기반",
    "사번 로그인":    "사내 계정 로그인",
    "땡겨요":        "자체 플랫폼 서비스",
    "신한":          "금융권 A사",
}

# ── 4. 제품명 익명화 ──────────────────────────────────────────────
PRODUCT_MAP = {
    "택가이코드 어시스턴트": "사내 AI 코딩 도구",
    "택가이코드":  "사내 AI 코딩 도구",
    "택가이 코드": "사내 AI 코딩 도구",
    "택가이웹":    "사내 AI 포털",
    "택가이 웹":   "사내 AI 포털",
    "택가이":      "사내 AI 도구",
    "TECHAI CODE": "AI CODING TOOL",
    "TechAI Code": "AI Coding Tool",
    "TECHAI":      "AI CODING",
    "TechAI":      "AI Coding",
    "techai":      "aicoding",
    "TGC":         "AICT",
}

# 텍스트로 치환하면 안 되는 것: 파일 경로/속성값. 먼저 토큰으로 뺀다.
PROTECT_RE = re.compile(
    r'(?:src|href|poster|data-src|content)\s*=\s*"[^"]*"'
    r'|assets/[A-Za-z0-9_.\-/]+'
    r'|url\((?:[^)]*)\)'
)

FORBIDDEN = (NAMES + ["신한", "TECH혁신UNIT", "AX CELL", "GITSOP", "스윙 SSO",
             "행내", "땡겨요", "택가이", "사번",
             "디지털서비스개발", "정보서비스개발", "글로벌서비스개발",
             "투자서비스개발", "금융서비스개발", "여신서비스개발",
             "기관·제휴개발", "투자자산수탁", "고객마케팅", "신탁솔루션",
             "AX디지털솔루션", "AX·디지털솔루션", "AX 디지털솔루션",
             "ICT아웃소싱", "땡겨요사업단"])


def protect(html):
    store = []
    def keep(m):
        store.append(m.group(0))
        return f"\x00P{len(store)-1}\x00"
    return PROTECT_RE.sub(keep, html), store


def restore(html, store):
    for i, v in enumerate(store):
        html = html.replace(f"\x00P{i}\x00", v)
    return html


def strip_blur(html):
    """blur 필터 제거 — 문자열을 이미 치환했으므로 흐릴 이유가 없다."""
    html = re.sub(r'display:inline-block;filter:blur\(\d+px\);?', '', html)
    html = re.sub(r'filter:blur\(\d+px\);?', '', html)
    return html


def transform(html):
    html, store = protect(html)
    for table in (ORG_MAP, DEPT_MAP, PRODUCT_MAP, NAME_MAP):
        for k in sorted(table, key=len, reverse=True):
            html = html.replace(k, table[k])
    html = restore(html, store)
    return strip_blur(html)


def main():
    # 덱 폴더만 갈아엎는다. 뷰어(index.html)와 대조 페이지(compare.html)는 손대지 않는다.
    OUT.mkdir(parents=True, exist_ok=True)
    for d in DECKS:
        if (OUT / d).exists():
            shutil.rmtree(OUT / d)

    report = {}
    for d in DECKS:
        src_dir = ROOT / d
        dst_dir = OUT / d
        dst_dir.mkdir(parents=True, exist_ok=True)
        # assets는 심볼릭이 아니라 실제 복사 (Vercel이 symlink를 따라가지 않음)
        shutil.copytree(src_dir / "assets", dst_dir / "assets")

        raw = (src_dir / "index.html").read_text(encoding="utf-8")
        out = transform(raw)
        (dst_dir / "index.html").write_text(out, encoding="utf-8")

        hits = {k: out.count(k) for k in FORBIDDEN if out.count(k)}
        report[d] = {
            "원본_bytes": len(raw.encode()),
            "모자이크_bytes": len(out.encode()),
            "blur_남음": len(re.findall(r'blur\(', out)),
            "금칙어_잔존": hits,
        }
        print(f"[{d}] {len(raw)}자 -> {len(out)}자 · blur {len(re.findall(chr(98)+'lur.', out))}건 · 금칙어 {len(hits)}종")
        for k, v in hits.items():
            print(f"    ! {k} x{v}")

    (OUT / "_build_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n리포트:", OUT / "_build_report.json")
    return 0 if not any(r["금칙어_잔존"] for r in report.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
