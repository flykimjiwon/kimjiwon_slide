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


# ── 5. 원본으로 되돌아가는 출구 차단 ──────────────────────────────
# 덱 안에는 원본 배포 URL과 원본 PDF 링크가 박혀 있다. 그대로 두면
# 모자이크본을 열람하다 한 번의 클릭으로 마스킹 안 된 원본에 도달한다.
def cut_escape_hatches(html, deck):
    # (a) 원본 덱 배포 URL -> 공개본으로
    html = html.replace(f"https://kimjiwon-slide.vercel.app/{deck}",
                        "https://kimjiwon-slide.vercel.app/sbtifull")
    html = html.replace(f"kimjiwon-slide.vercel.app/{deck}",
                        "kimjiwon-slide.vercel.app/sbtifull")

    # (b) 원본 PDF 다운로드 버튼 통째로 제거 (PDF 자체도 공개본에서 뺀다)
    html = re.sub(r'<a\b[^>]*href="assets/' + deck + r'\.pdf"[^>]*>.*?</a>',
                  '', html, flags=re.S)

    # (c) 첨부 파일·외부 배포 URL을 실제로 걸고 있는 슬라이드만 제거한다.
    #     타운홀·부서장회의 별첨 5종과 제품명이 드러나는 외부 URL이 여기 모여 있다.
    #     링크가 없는 단순 구분용 부록 슬라이드(sbti2)는 본문이므로 건드리지 않는다.
    def drop_if_links_out(m):
        sec = m.group(0)
        leaks = re.search(r'href="[^"]*(?:attachments/|techai-code\.|harnesstgc\.'
                          r'|baedal-blush\.|axslide\.|/agentmake)', sec)
        return "" if leaks else sec

    html = re.sub(r'<section class="slide[^"]*".*?</section>',
                  drop_if_links_out, html, flags=re.S)
    return html


# 공개본 assets에서 통째로 빼는 것 — 원본 PDF와 미검수 별첨 자료
ASSET_DENY_SUFFIX = (".pdf",)
ASSET_DENY_DIRS = ("attachments",)


def prune_assets(dst_dir):
    removed = []
    for p in sorted(dst_dir.rglob("*")):
        if p.is_dir():
            continue
        if p.suffix.lower() in ASSET_DENY_SUFFIX or \
           any(part in ASSET_DENY_DIRS for part in p.parts):
            removed.append(p.relative_to(dst_dir))
            p.unlink()
    for d in ASSET_DENY_DIRS:
        t = dst_dir / "assets" / d
        if t.exists():
            shutil.rmtree(t)
    return removed


def transform(html, deck):
    html = cut_escape_hatches(html, deck)
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

        pruned = prune_assets(dst_dir)

        raw = (src_dir / "index.html").read_text(encoding="utf-8")
        out = transform(raw, d)
        (dst_dir / "index.html").write_text(out, encoding="utf-8")

        hits = {k: out.count(k) for k in FORBIDDEN if out.count(k)}
        # 원본으로 되돌아가는 링크가 남았는지 — 이게 남으면 마스킹이 무의미해진다
        escapes = re.findall(r'(?:href|src)="([^"]*(?:'
                             r'vercel\.app/sbti[123]|assets/sbti[123]\.pdf|attachments/'
                             r')[^"]*)"', out)
        # 참조는 하는데 파일이 없는 것
        broken = [a for a in set(re.findall(r'(?:href|src)="(assets/[^"]+)"', out))
                  if not (dst_dir / a).exists()]
        report[d] = {
            "원본_bytes": len(raw.encode()),
            "모자이크_bytes": len(out.encode()),
            "blur_남음": len(re.findall(r'blur\(', out)),
            "금칙어_잔존": hits,
            "원본_역링크_잔존": escapes,
            "깨진_참조": broken,
            "제외한_에셋": [str(p) for p in pruned],
        }
        print(f"[{d}] {len(raw)}자 -> {len(out)}자 · 금칙어 {len(hits)}종 · "
              f"역링크 {len(escapes)}건 · 깨진참조 {len(broken)}건 · 에셋제외 {len(pruned)}개")
        for k, v in hits.items():
            print(f"    ! 금칙어 {k} x{v}")
        for e in escapes:
            print(f"    ! 원본 역링크 {e}")
        for b in broken:
            print(f"    ! 깨진 참조 {b}")
        for p in pruned:
            print(f"      - 제외 {p}")

    (OUT / "_build_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n리포트:", OUT / "_build_report.json")
    fail = any(r["금칙어_잔존"] or r["원본_역링크_잔존"] or r["깨진_참조"]
               for r in report.values())
    print("판정:", "실패 — 위 항목을 해결할 것" if fail else "통과")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
