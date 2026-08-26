#!/usr/bin/env python3
"""easyai 원본 -> easyaifull 모자이크본 생성. 원본 easyai/는 읽기만 한다.

sbti1~3와 달리 easyai는 <base> 태그가 없는 스크롤형 단일 페이지라
build_sbtifull.py의 덱 목록에 넣지 않고 이 스크립트가 따로 만든다.
치환 규칙·보호 패턴·금칙어 목록은 build_sbtifull.py의 것을 그대로 가져다 쓴다.

usage: python3 scripts/build_easyaifull.py
"""
import re, shutil, sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_sbtifull import (ROOT, NAME_MAP, DEPT_MAP, ORG_MAP, PRODUCT_MAP,
                            FORBIDDEN, protect, restore, stamp)

SRC = ROOT / "easyai"
OUT = ROOT / "easyaifull"


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    raw = (SRC / "index.html").read_text(encoding="utf-8")

    html = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
    # 자기 참조 링크가 원본 /easyai로 나가지 않게
    html = html.replace("kimjiwon-slide.vercel.app/easyai",
                        "kimjiwon-slide.vercel.app/easyaifull")
    # LICENSE 링크가 GitHub의 원본 easyai/ 경로로 나가던 것 — 사본을 동봉하고 상대링크로
    html = html.replace("https://github.com/flykimjiwon/kimjiwon_slide/blob/main/easyai/LICENSE",
                        "LICENSE")
    shutil.copy2(SRC / "LICENSE", OUT / "LICENSE")
    # <base> 주입 — cleanUrls · trailingSlash:false 배포에서는 주소가
    # /easyaifull(뒤 슬래시 없음)에 머물러 상대경로가 / 기준으로 풀린다.
    # base가 없으면 assets/ 참조가 전부 루트로 새는 sbtifull 2a2df49 계열 사고.
    html = re.sub(r'(<head[^>]*>)', r'\1<base href="/easyaifull/">', html, count=1)

    html, store = protect(html)
    for table in (ORG_MAP, DEPT_MAP, PRODUCT_MAP, NAME_MAP):
        for k in sorted(table, key=len, reverse=True):
            html = html.replace(k, table[k])
    html = restore(html, store)
    html = stamp(html)
    (OUT / "index.html").write_text(html, encoding="utf-8")

    # 참조된 에셋만 복사 — 원본 assets 154MB 중 실사용분만.
    # PROVENANCE.md·DESIGN.md·원본 PDF·visual-options/ 등 내부 유래 기록은 대상 자체가 아니다.
    refs = sorted(set(re.findall(r'(?:src|href)="(assets/[^"]+)"', html)))
    copied, broken = [], []
    for rel in refs:
        s, d = SRC / rel, OUT / rel
        if not s.exists():
            broken.append(rel)
            continue
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        copied.append(rel)

    # 검증 — base64 data URI 속 우연한 문자열(TGC 등 3~4자 조합)은 금칙어가
    # 아니므로 제외하고 센다. 실제 텍스트·경로 잔존만 잡는다.
    scan = re.sub(r'(?:src|href)="data:[^"]*"', '', html)
    scan = re.sub(r'url\((?:&quot;|["\'])?data:[^)]*\)', '', scan)
    hits = {k: scan.count(k) for k in FORBIDDEN if scan.count(k)}
    escapes = re.findall(r'(?:href|src)="([^"]*(?:vercel\.app/easyai(?!full)|/easyai/)[^"]*)"',
                         html)

    report = {
        "원본_bytes": len(raw.encode()),
        "모자이크_bytes": len(html.encode()),
        "금칙어_잔존": hits,
        "원본_역링크_잔존": escapes,
        "깨진_참조": broken,
        "복사한_에셋": copied,
    }
    (OUT / "_build_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[easyai] {len(raw)}자 -> {len(html)}자 · 금칙어 {len(hits)}종 · "
          f"역링크 {len(escapes)}건 · 깨진참조 {len(broken)}건 · 에셋복사 {len(copied)}개")
    for k, v in hits.items():
        print(f"    ! 금칙어 {k} x{v}")
    for e in escapes:
        print(f"    ! 원본 역링크 {e}")
    for b in broken:
        print(f"    ! 깨진 참조 {b}")
    fail = bool(hits or escapes or broken)
    print("판정:", "실패 — 위 항목을 해결할 것" if fail else "통과")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
