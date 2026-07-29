#!/usr/bin/env python3
"""
SBTI 강사 가이드 사이트 빌더

_source/data/*.md 를 읽어 자체 완결(single-file) HTML 가이드 사이트를 만든다.
외부 네트워크 의존성 없음 — 폐쇄망 노트북에서 파일을 더블클릭해도 그대로 열린다.

    python3 build.py            # -> index.html

디자인 방향: "브리핑 도크" — 관제실 문서. 잉크블랙 캔버스 + 시그널 앰버 단일 강조색,
헤어라인 괘선, 여백에 떠 있는 고스트 넘버, 메타데이터는 전부 모노스페이스.
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "_source" / "data"
OUT = ROOT / "index.html"

BUILD_DATE = "2026-07-29"

# 권(volume) 구성 — (파일명, 로마숫자, 짧은라벨, 한줄설명, 언제보나)
VOLUMES = [
    ("10_통합브리핑.md", "I", "통합 브리핑",
     "두 조사의 교차검증 · P0 차단항목 · 3일 골격", "지금 먼저"),
    ("20_트렌드_지식브리핑.md", "II", "트렌드 지식브리핑",
     "하네스 · MCP · 멀티에이전트 · 키워드 사전 130+", "도메인 지식"),
    ("30_강사_마스터가이드.md", "III", "강사 마스터 가이드",
     "시스템 계층 · 프로토콜 스택 · 평가 · 거버넌스", "심화·정합성"),
    ("40_강사_학습노트.md", "IV", "학습노트 & Q&A",
     "안전 브리핑 원문 · 기본 예상 질문", "강의 직전"),
    ("50_강의_운영준비.md", "V", "강의 운영 준비",
     "시간표 · 인력 · 장애 대응 · 체크리스트", "운영 설계"),
    ("60_40석_리허설.md", "VI", "40석 리허설",
     "T-7 리허설 시나리오와 GO/NO-GO 기준", "리허설 당일"),
    ("70_근거팩_템플릿.md", "VII", "수치·주장 근거팩",
     "숫자 질문 방어용 클레임 카드", "숫자 질문 대비"),
    ("80_참가자_사전안내.md", "VIII", "참가자 사전안내",
     "참가자에게 그대로 발송하는 안내문", "T-3 발송"),
    ("90_슬라이드_원문.md", "IX", "슬라이드 원문",
     "sbti1·2·3 텍스트 전문 (부록)", "문장 대조"),
]

# ─────────────────────────────────────────────────────────────────────────────
# 마크다운 렌더러 (이 문서 세트가 실제로 쓰는 문법만 지원)
# ─────────────────────────────────────────────────────────────────────────────

GRADE_CHIPS = {
    "🟢": ("g-a", "A"),
    "🟡": ("g-b", "B"),
    "🔴": ("g-e", "E"),
}
FLAG_ICONS = {"⚠️": "warn", "🚨": "alert", "🔍": "note", "⏳": "note",
              "🥇": "rank", "🥈": "rank", "🎓": "note", "📋": "note"}


def esc(t: str) -> str:
    return html.escape(t, quote=False)


# 제목에서는 같은 이모지가 "근거 등급"이 아니라 "경보 표시"로 쓰인다.
HEADING_DOTS = {"🟢": "ok", "🟡": "warn", "🔴": "alert"}


def inline(t: str, heading: bool = False) -> str:
    """인라인 마크다운 → HTML. 코드 스팬을 먼저 격리해 내부 마크업을 보호한다."""
    spans: list[str] = []

    def stash(m):
        spans.append(f'<code>{esc(m.group(1))}</code>')
        return f"\x00{len(spans) - 1}\x00"

    t = re.sub(r"`([^`]+)`", stash, t)
    t = esc(t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link, t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", t)
    if heading:
        for emoji, cls in HEADING_DOTS.items():
            t = t.replace(emoji, f'<span class="ico {cls}" aria-hidden="true"></span>')
    else:
        # 본문에서는 등급 칩
        for emoji, (cls, label) in GRADE_CHIPS.items():
            t = t.replace(
                emoji, f'<span class="chip {cls}" title="근거 등급 {label}">{label}</span>')
    for emoji, cls in FLAG_ICONS.items():
        t = t.replace(emoji, f'<span class="ico {cls}" aria-hidden="true"></span>')
    t = re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], t)
    return t


def _link(m):
    text, href = m.group(1), m.group(2)
    if href.startswith(("http://", "https://")):
        return (f'<a href="{esc(href)}" target="_blank" rel="noopener noreferrer" '
                f'class="ext">{text}<span class="ext-mark">↗</span></a>')
    return f'<a href="{esc(href)}" class="loc">{text}</a>'


def slugify(text: str, seen: dict) -> str:
    s = re.sub(r"[^\w가-힣]+", "-", text.strip().lower()).strip("-") or "s"
    n = seen.get(s, 0)
    seen[s] = n + 1
    return s if n == 0 else f"{s}-{n}"


class Renderer:
    def __init__(self, vol_idx: str):
        self.vol = vol_idx
        self.out: list[str] = []
        self.nav: list[dict] = []
        self.seen: dict = {}
        self.h2_count = 0

    # -- helpers ------------------------------------------------------------
    def _row(self, line, tag="td", aligns=None):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        html_cells = []
        for i, c in enumerate(cells):
            a = aligns[i] if aligns and i < len(aligns) else ""
            style = f' class="{a}"' if a else ""
            html_cells.append(f"<{tag}{style}>{inline(c)}</{tag}>")
        return "<tr>" + "".join(html_cells) + "</tr>"

    # -- main ---------------------------------------------------------------
    def render(self, md: str) -> str:
        lines = md.split("\n")
        i, n = 0, len(lines)
        while i < n:
            line = lines[i]

            # fenced code
            if line.startswith("```"):
                lang = line[3:].strip()
                i += 1
                buf = []
                while i < n and not lines[i].startswith("```"):
                    buf.append(lines[i])
                    i += 1
                i += 1
                label = f'<span class="code-lang">{esc(lang)}</span>' if lang else ""
                self.out.append(
                    f'<figure class="code">{label}<pre><code>'
                    f'{esc(chr(10).join(buf))}</code></pre></figure>')
                continue

            # heading
            m = re.match(r"^(#{1,6})\s+(.*)$", line)
            if m:
                lvl, text = len(m.group(1)), m.group(2).strip()
                plain = re.sub(r"[`*\[\]]|\(https?://[^)]+\)", "", text)
                plain = re.sub(r"[🟢🟡🔴⚠️🚨🔍⏳🥇🥈🎓📋]", "", plain).strip()
                if lvl == 1:
                    self.out.append(f'<h1 class="vol-title">{inline(text, True)}</h1>')
                    i += 1
                    continue
                sid = f"v{self.vol}-{slugify(plain, self.seen)}"
                if lvl == 2:
                    self.h2_count += 1
                    self.nav.append({"id": sid, "t": plain, "l": 2})
                    # 여백 표시는 자동 번호가 아니라 "지금 몇 권인가" 방향 표시다.
                    # 원문 제목이 이미 번호를 갖고 있어 자동 번호를 붙이면 충돌한다.
                    self.out.append(
                        f'<section class="sec" id="{sid}">'
                        f'<div class="sec-num" aria-hidden="true"><span>{self.vol}</span></div>'
                        f'<h2>{inline(text, True)}</h2>')
                    # 다음 h2 전까지가 섹션 — 닫기는 마지막에 일괄
                    self.out.append("<!--SECOPEN-->")
                elif lvl == 3:
                    self.nav.append({"id": sid, "t": plain, "l": 3})
                    self.out.append(f'<h3 id="{sid}">{inline(text)}</h3>')
                else:
                    self.out.append(f'<h4 id="{sid}">{inline(text)}</h4>')
                i += 1
                continue

            # table
            if line.strip().startswith("|") and i + 1 < n and re.match(
                    r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
                header = line
                sep = lines[i + 1]
                aligns = []
                for c in sep.strip().strip("|").split("|"):
                    c = c.strip()
                    aligns.append("ta-r" if c.endswith(":") and not c.startswith(":")
                                  else "ta-c" if c.startswith(":") and c.endswith(":")
                                  else "")
                i += 2
                body = []
                while i < n and lines[i].strip().startswith("|"):
                    body.append(self._row(lines[i], "td", aligns))
                    i += 1
                self.out.append(
                    '<div class="tw"><table>'
                    f'<thead>{self._row(header, "th", aligns)}</thead>'
                    f'<tbody>{"".join(body)}</tbody></table></div>')
                continue

            # blockquote
            if line.startswith(">"):
                buf = []
                while i < n and lines[i].startswith(">"):
                    buf.append(lines[i].lstrip(">").strip())
                    i += 1
                inner = " ".join(x for x in buf if x)
                self.out.append(f"<blockquote><p>{inline(inner)}</p></blockquote>")
                continue

            # hr
            if re.match(r"^\s*---+\s*$", line):
                self.out.append('<hr class="rule">')
                i += 1
                continue

            # list (ul / ol / checkbox), 1단계 중첩까지
            if re.match(r"^\s*(?:[-*]|\d+\.)\s+", line):
                i = self._list(lines, i)
                continue

            # paragraph
            if line.strip():
                buf = []
                while i < n and lines[i].strip() and not re.match(
                        r"^\s*(?:#{1,6}\s|[-*]\s|\d+\.\s|>|```|\||---+\s*$)", lines[i]):
                    buf.append(lines[i].strip())
                    i += 1
                if buf:
                    self.out.append(f'<p>{inline(" ".join(buf))}</p>')
                    continue
            i += 1

        body = "\n".join(self.out)
        # 섹션 닫기: 열린 마커를 순차 처리
        parts = body.split("<!--SECOPEN-->")
        if len(parts) > 1:
            body = parts[0] + "<!--SECOPEN-->".join(parts[1:])
            body = body.replace("<!--SECOPEN-->", "")
            # 각 <section class="sec" 앞에 </section> 삽입 (첫 번째 제외) + 끝에 하나
            chunks = body.split('<section class="sec"')
            body = chunks[0] + "".join(
                f'</section><section class="sec"{c}' if k > 0 else f'<section class="sec"{c}'
                for k, c in enumerate(chunks[1:]))
            body += "</section>"
        return body

    def _list(self, lines, i):
        n = len(lines)
        ordered = bool(re.match(r"^\s*\d+\.\s", lines[i]))
        items, stack_open = [], False
        while i < n and re.match(r"^\s*(?:[-*]|\d+\.)\s+", lines[i]):
            raw = lines[i]
            indent = len(raw) - len(raw.lstrip())
            text = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", raw).rstrip()
            # 이어지는 들여쓰기 본문 줄 흡수
            j = i + 1
            while (j < n and lines[j].strip()
                   and not re.match(r"^\s*(?:[-*]|\d+\.)\s+", lines[j])
                   and (len(lines[j]) - len(lines[j].lstrip())) > indent):
                text += " " + lines[j].strip()
                j += 1
            i = j
            cb = re.match(r"^\[([ xX])\]\s*(.*)$", text)
            if cb:
                done = cb.group(1).lower() == "x"
                text = (f'<label class="cbx"><span class="box{" on" if done else ""}"></span>'
                        f'<span>{inline(cb.group(2))}</span></label>')
            else:
                text = inline(text)
            if indent >= 2:
                if not stack_open:
                    items.append("<ul class='sub'>")
                    stack_open = True
                items.append(f"<li>{text}</li>")
            else:
                if stack_open:
                    items.append("</ul>")
                    stack_open = False
                items.append(f"<li>{text}</li>")
        if stack_open:
            items.append("</ul>")
        tag = "ol" if ordered else "ul"
        self.out.append(f"<{tag}>{''.join(items)}</{tag}>")
        return i


# ─────────────────────────────────────────────────────────────────────────────
# 셸
# ─────────────────────────────────────────────────────────────────────────────

CSS = r"""
*,*::before,*::after{box-sizing:border-box}
:root{
  --ink:#0a0b0d; --ink2:#101216; --ink3:#161920; --line:#252932;
  --fg:#e7e4dd; --fg2:#a8a79f; --fg3:#6f6f6a;
  --amber:#e8a33d; --amber-dim:#8a622a; --red:#e0614a; --green:#69a67d; --blue:#6d93c4;
  --sel:rgba(232,163,61,.22);
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,"Cascadia Mono",monospace;
  --sans:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,
         "Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif;
  --rail:302px; --measure:74ch;
}
html[data-theme="light"]{
  --ink:#f4f1ea; --ink2:#ebe7de; --ink3:#e2ddd2; --line:#d3ccbd;
  --fg:#1a1a18; --fg2:#54534d; --fg3:#84837c;
  --amber:#9a6410; --amber-dim:#c39a4e; --red:#a8341c; --green:#3d6b4c; --blue:#2f5484;
  --sel:rgba(154,100,16,.16);
}
html{scroll-behavior:smooth;scroll-padding-top:24px;-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--ink);color:var(--fg);font-family:var(--sans);
  font-size:16px;line-height:1.78;letter-spacing:-.011em;
  font-feature-settings:"tnum" 1,"case" 1;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
}
body::before{ /* 그레인 */
  content:"";position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.032;
  background-image:radial-gradient(circle at 1px 1px,#fff 1px,transparent 0);
  background-size:3px 3px;
}
html[data-theme="light"] body::before{opacity:.05;
  background-image:radial-gradient(circle at 1px 1px,#000 1px,transparent 0)}
::selection{background:var(--sel)}

/* ── 진행 바 ─────────────────────────────── */
#prog{position:fixed;top:0;left:0;height:2px;width:0;z-index:90;
  background:linear-gradient(90deg,var(--amber-dim),var(--amber));transition:width .12s linear}

/* ── 레일 ────────────────────────────────── */
#rail{
  position:fixed;inset:0 auto 0 0;width:var(--rail);z-index:60;
  background:var(--ink2);border-right:1px solid var(--line);
  display:flex;flex-direction:column;
}
.rail-head{padding:26px 24px 18px;border-bottom:1px solid var(--line)}
.brand{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;
  text-transform:uppercase;color:var(--amber);margin:0 0 10px}
.rail-head h1{margin:0;font-size:19px;line-height:1.32;font-weight:800;letter-spacing:-.028em}
.rail-head .meta{margin:9px 0 0;font-family:var(--mono);font-size:10.5px;
  color:var(--fg3);letter-spacing:.03em;line-height:1.7}
.search{position:relative;padding:14px 18px;border-bottom:1px solid var(--line)}
.search input{
  width:100%;background:var(--ink3);border:1px solid var(--line);color:var(--fg);
  font-family:var(--sans);font-size:13px;padding:9px 30px 9px 11px;border-radius:3px;outline:none}
.search input:focus{border-color:var(--amber-dim);box-shadow:0 0 0 3px var(--sel)}
.search input::placeholder{color:var(--fg3)}
.search kbd{position:absolute;right:27px;top:23px;font-family:var(--mono);font-size:10px;
  color:var(--fg3);border:1px solid var(--line);border-radius:3px;padding:1px 5px;pointer-events:none}
.search.on kbd{display:none}
#hits{padding:0 18px;font-family:var(--mono);font-size:10.5px;color:var(--amber);
  height:0;overflow:hidden;transition:height .16s}
.search.on ~ #hits{height:26px;line-height:26px}
nav{flex:1;overflow-y:auto;padding:12px 0 40px;scrollbar-width:thin}
nav::-webkit-scrollbar{width:7px}nav::-webkit-scrollbar-thumb{background:var(--line);border-radius:4px}
.vgrp{border-bottom:1px solid var(--line)}
.vhead{display:flex;gap:10px;align-items:baseline;width:100%;background:none;border:0;
  color:var(--fg);text-align:left;cursor:pointer;padding:12px 18px;font-family:var(--sans);
  font-size:13.5px;font-weight:700;letter-spacing:-.02em}
.vhead:hover{background:var(--ink3)}
.vhead .rn{font-family:var(--mono);font-size:10px;color:var(--amber);letter-spacing:.1em;
  min-width:26px;font-weight:600}
.vhead .cnt{margin-left:auto;font-family:var(--mono);font-size:9.5px;color:var(--fg3)}
.vhead .desc{display:block;font-weight:400;font-size:11px;color:var(--fg3);
  letter-spacing:0;margin-top:2px}
.vbody{display:none;padding:0 0 10px}
.vgrp.open .vbody{display:block}
.vbody a{display:block;padding:5px 18px 5px 54px;color:var(--fg2);text-decoration:none;
  font-size:12.5px;line-height:1.5;border-left:2px solid transparent}
.vbody a.l3{padding-left:66px;font-size:11.5px;color:var(--fg3)}
.vbody a:hover{color:var(--fg);background:var(--ink3)}
.vbody a.active{color:var(--amber);border-left-color:var(--amber);background:var(--ink3)}
.rail-foot{padding:12px 18px;border-top:1px solid var(--line);display:flex;gap:8px;align-items:center}
.btn{background:var(--ink3);border:1px solid var(--line);color:var(--fg2);cursor:pointer;
  font-family:var(--mono);font-size:10px;letter-spacing:.08em;padding:6px 10px;border-radius:3px}
.btn:hover{color:var(--amber);border-color:var(--amber-dim)}

/* ── 본문 ────────────────────────────────── */
main{margin-left:var(--rail);position:relative;z-index:1}
.wrap{max-width:calc(var(--measure) + 200px);padding:0 72px 160px 130px}
header.hero{padding:96px 0 54px;border-bottom:1px solid var(--line);margin-bottom:8px}
.hero .kicker{font-family:var(--mono);font-size:10.5px;letter-spacing:.24em;
  text-transform:uppercase;color:var(--amber);margin:0 0 22px}
.hero h1{margin:0;font-size:clamp(34px,4.6vw,58px);line-height:1.08;font-weight:850;
  letter-spacing:-.042em}
.hero h1 em{font-style:normal;color:var(--amber)}
.hero .sub{margin:22px 0 0;font-size:16.5px;color:var(--fg2);max-width:60ch;line-height:1.72}
.facts{display:flex;flex-wrap:wrap;gap:0;margin:38px 0 0;border-top:1px solid var(--line)}
.fact{padding:16px 26px 16px 0;margin-right:26px;border-right:1px solid var(--line)}
.fact:last-child{border-right:0}
.fact b{display:block;font-family:var(--mono);font-size:23px;font-weight:600;
  letter-spacing:-.03em;color:var(--fg)}
.fact span{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--fg3);margin-top:5px}

.vol{padding-top:76px;scroll-margin-top:0}
.vol-tag{display:flex;align-items:baseline;gap:14px;margin-bottom:6px}
.vol-tag .rn{font-family:var(--mono);font-size:11px;letter-spacing:.2em;color:var(--amber)}
.vol-tag .ln{flex:1;height:1px;background:var(--line)}
.vol-tag .when{font-family:var(--mono);font-size:10px;color:var(--fg3);letter-spacing:.08em}
h1.vol-title{font-size:clamp(26px,3vw,38px);line-height:1.16;font-weight:820;
  letter-spacing:-.036em;margin:0 0 34px}

.sec{position:relative;padding-top:46px}
/* 여백 레일 — 현재 "권"을 따라다니며 알려주는 방향 표시 */
.sec-num{position:absolute;left:-98px;top:52px;bottom:0;width:62px;
  user-select:none;pointer-events:none}
.sec-num span{position:sticky;top:30px;display:block;font-family:var(--mono);
  font-size:10.5px;font-weight:600;letter-spacing:.26em;color:var(--fg3);
  padding-top:13px;border-top:1px solid var(--line)}
h2{font-size:24px;line-height:1.32;font-weight:800;letter-spacing:-.03em;
  margin:0 0 20px;padding-bottom:12px;border-bottom:1px solid var(--line)}
h3{font-size:17.5px;line-height:1.42;font-weight:750;letter-spacing:-.024em;margin:38px 0 14px;
  color:var(--fg)}
h4{font-size:14.5px;font-weight:700;letter-spacing:.01em;margin:26px 0 10px;color:var(--fg2)}
p{margin:0 0 17px;max-width:var(--measure)}
a.ext{color:var(--blue);text-decoration:none;border-bottom:1px solid rgba(109,147,196,.32)}
a.ext:hover{border-bottom-color:var(--blue)}
.ext-mark{font-size:.78em;margin-left:2px;opacity:.6}
a.loc{color:var(--fg2);text-decoration:none;border-bottom:1px dotted var(--fg3)}
strong{font-weight:750;color:#fff}
html[data-theme="light"] strong{color:#000}
em{font-style:normal;color:var(--fg2)}
code{font-family:var(--mono);font-size:.855em;background:var(--ink3);color:var(--amber);
  padding:1.5px 5px;border-radius:3px;border:1px solid var(--line);white-space:nowrap}
hr.rule{border:0;height:1px;background:var(--line);margin:44px 0}

ul,ol{margin:0 0 18px;padding-left:1.35em;max-width:var(--measure)}
li{margin:0 0 7px}
li::marker{color:var(--amber-dim);font-family:var(--mono);font-size:.86em}
ul.sub{margin:7px 0 4px;padding-left:1.2em}
ul.sub li::marker{color:var(--fg3)}
.cbx{display:flex;gap:9px;align-items:flex-start}
.cbx .box{flex:none;width:13px;height:13px;margin-top:5px;border:1px solid var(--fg3);
  border-radius:2px;position:relative}
.cbx .box.on{border-color:var(--green);background:var(--green)}
.cbx .box.on::after{content:"";position:absolute;left:3.6px;top:.8px;width:3.5px;height:7px;
  border:solid var(--ink);border-width:0 1.8px 1.8px 0;transform:rotate(42deg)}

blockquote{margin:24px 0;padding:16px 22px;border-left:2px solid var(--amber);
  background:var(--ink2);max-width:var(--measure)}
blockquote p{margin:0;color:var(--fg);font-size:15.5px}

figure.code{margin:22px 0;position:relative;max-width:var(--measure)}
.code-lang{position:absolute;top:0;right:0;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--fg3);
  background:var(--ink3);border:1px solid var(--line);border-width:0 0 1px 1px;padding:3px 9px}
figure.code pre{margin:0;background:var(--ink2);border:1px solid var(--line);border-radius:3px;
  padding:18px 20px;overflow-x:auto}
figure.code code{background:none;border:0;padding:0;color:var(--fg2);font-size:12.6px;
  line-height:1.72;white-space:pre}

.tw{overflow-x:auto;margin:22px 0;border:1px solid var(--line);border-radius:3px}
table{border-collapse:collapse;width:100%;font-size:13.6px;line-height:1.6}
th{background:var(--ink3);text-align:left;font-weight:700;font-size:11.5px;letter-spacing:.04em;
  text-transform:uppercase;color:var(--fg2);padding:11px 14px;border-bottom:1px solid var(--line);
  white-space:nowrap}
td{padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:top}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--ink2)}
.ta-r{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
.ta-c{text-align:center}

.chip{display:inline-block;font-family:var(--mono);font-size:9.5px;font-weight:700;
  letter-spacing:.09em;padding:1.5px 6px;border-radius:2px;vertical-align:2px;margin-right:3px}
.chip.g-a{background:rgba(105,166,125,.16);color:var(--green);border:1px solid rgba(105,166,125,.36)}
.chip.g-b{background:rgba(232,163,61,.14);color:var(--amber);border:1px solid rgba(232,163,61,.34)}
.chip.g-e{background:rgba(224,97,74,.14);color:var(--red);border:1px solid rgba(224,97,74,.36)}
.ico{display:inline-block;width:9px;height:9px;margin-right:6px;vertical-align:1px;border-radius:1px}
h2 .ico{width:8px;height:8px;vertical-align:3px}
h3 .chip,h4 .chip{vertical-align:3px;margin-left:4px;margin-right:0}
.ico.warn{background:var(--amber)}
.ico.alert{background:var(--red);box-shadow:0 0 0 3px rgba(224,97,74,.16)}
.ico.ok{background:var(--green)}
.ico.note{background:var(--fg3)}
.ico.rank{background:var(--blue)}

/* 검색 */
.hide{display:none !important}
mark{background:var(--sel);color:var(--amber);padding:0 2px;border-radius:2px}

.tail{margin-top:110px;padding-top:26px;border-top:1px solid var(--line);
  font-family:var(--mono);font-size:10.5px;color:var(--fg3);letter-spacing:.05em;line-height:1.9}

#top{position:fixed;right:26px;bottom:26px;z-index:70;width:38px;height:38px;border-radius:3px;
  background:var(--ink3);border:1px solid var(--line);color:var(--fg2);cursor:pointer;
  font-size:15px;opacity:0;pointer-events:none;transition:opacity .2s}
#top.on{opacity:1;pointer-events:auto}
#top:hover{color:var(--amber);border-color:var(--amber-dim)}

@media (max-width:1180px){
  :root{--rail:0px}
  #rail{transform:translateX(-302px);width:302px;transition:transform .22s}
  #rail.open{transform:none;box-shadow:0 0 0 100vmax rgba(0,0,0,.55)}
  .wrap{padding:0 24px 120px;max-width:100%}
  .sec-num{display:none}
  main{overflow-x:hidden}          /* 표가 페이지 자체를 밀지 않게 */
  .tw{max-width:100%}
  code{white-space:normal;overflow-wrap:anywhere}
  .facts{gap:0 4px}
  #menu{display:block}
}
#menu{display:none;position:fixed;left:16px;top:16px;z-index:80}

@media print{
  #rail,#top,#prog,#menu{display:none}
  body{background:#fff;color:#000;font-size:10.5pt}
  body::before{display:none}
  main{margin:0}.wrap{padding:0;max-width:none}
  .sec-num{display:none}
  a.ext{color:#000}.ext-mark{display:none}
  .sec,h2,h3,table{break-inside:avoid}
  figure.code pre,.tw{border-color:#bbb}
  th{background:#eee;color:#000}
}
"""

JS = r"""
(function(){
  var root=document.documentElement, KEY='sbti-guide-theme';
  try{var t=localStorage.getItem(KEY); if(t) root.setAttribute('data-theme',t);}catch(e){}
  document.getElementById('theme').onclick=function(){
    var cur=root.getAttribute('data-theme')==='light'?'dark':'light';
    root.setAttribute('data-theme',cur);
    try{localStorage.setItem(KEY,cur);}catch(e){}
  };

  // 권 아코디언
  document.querySelectorAll('.vhead').forEach(function(b){
    b.onclick=function(){ b.parentElement.classList.toggle('open'); };
  });
  var first=document.querySelector('.vgrp'); if(first) first.classList.add('open');

  // 진행 바 + top 버튼
  var prog=document.getElementById('prog'), top=document.getElementById('top');
  function onScroll(){
    var h=document.documentElement.scrollHeight-window.innerHeight;
    var p=h>0?(window.scrollY/h)*100:0;
    prog.style.width=p+'%';
    top.classList.toggle('on', window.scrollY>700);
  }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
  top.onclick=function(){window.scrollTo({top:0,behavior:'smooth'});};

  // 활성 섹션
  var links={}, targets=[];
  document.querySelectorAll('.vbody a').forEach(function(a){
    var id=a.getAttribute('href').slice(1); links[id]=a;
    var el=document.getElementById(id); if(el) targets.push(el);
  });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){
        var a=links[e.target.id]; if(!a) return;
        if(e.isIntersecting){
          Object.keys(links).forEach(function(k){links[k].classList.remove('active');});
          a.classList.add('active');
          if(!a.closest('.vgrp').classList.contains('open'))
            a.closest('.vgrp').classList.add('open');
        }
      });
    },{rootMargin:'-8% 0px -82% 0px'});
    targets.forEach(function(t){io.observe(t);});
  }

  // 검색
  var box=document.getElementById('q'), wrapS=document.querySelector('.search'),
      hits=document.getElementById('hits');
  var blocks=[].slice.call(document.querySelectorAll(
    'main p, main li, main blockquote, main .tw, main figure.code, main h3, main h4'));
  var origs=blocks.map(function(b){return b.innerHTML;});
  var secs=[].slice.call(document.querySelectorAll('.sec'));
  var vols=[].slice.call(document.querySelectorAll('.vol'));
  var timer;
  function clear(){
    blocks.forEach(function(b,i){b.innerHTML=origs[i]; b.classList.remove('hide');});
    secs.concat(vols).forEach(function(s){s.classList.remove('hide');});
    wrapS.classList.remove('on'); hits.textContent='';
  }
  function run(q){
    if(!q){clear();return;}
    wrapS.classList.add('on');
    var rx, n=0;
    try{ rx=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi'); }
    catch(e){ return; }
    blocks.forEach(function(b,i){
      var txt=b.textContent||'';
      if(txt.toLowerCase().indexOf(q.toLowerCase())>-1){
        b.classList.remove('hide'); n++;
        if(b.children.length===0 || b.tagName==='P' || b.tagName==='LI'
           || /^H[34]$/.test(b.tagName)){
          b.innerHTML=origs[i].replace(/>([^<]+)</g,function(m,t){
            return '>'+t.replace(rx,'<mark>$1</mark>')+'<';
          });
        }
      } else { b.classList.add('hide'); b.innerHTML=origs[i]; }
    });
    secs.forEach(function(s){
      var vis=s.querySelectorAll('p:not(.hide),li:not(.hide),blockquote:not(.hide),'+
        '.tw:not(.hide),figure.code:not(.hide),h3:not(.hide),h4:not(.hide)').length;
      var inHead=(s.querySelector('h2')||{textContent:''}).textContent
                  .toLowerCase().indexOf(q.toLowerCase())>-1;
      s.classList.toggle('hide', vis===0 && !inHead);
    });
    vols.forEach(function(v){
      v.classList.toggle('hide', v.querySelectorAll('.sec:not(.hide)').length===0);
    });
    hits.textContent=n>0?(n+'개 블록 일치 · Esc 해제'):'일치 없음';
  }
  box.addEventListener('input',function(){
    clearTimeout(timer); var v=box.value.trim();
    timer=setTimeout(function(){run(v);},140);
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='/' && document.activeElement!==box){e.preventDefault();box.focus();}
    if(e.key==='Escape'){box.value='';clear();box.blur();}
  });

  // 모바일 메뉴
  var rail=document.getElementById('rail');
  document.getElementById('menu').onclick=function(){rail.classList.toggle('open');};
  rail.addEventListener('click',function(e){
    if(e.target.tagName==='A' && window.innerWidth<=1180) rail.classList.remove('open');
  });
})();
"""


def build():
    nav_html, body_html = [], []
    total_secs = 0

    for fname, rn, label, desc, when in VOLUMES:
        path = DATA / fname
        if not path.exists():
            print(f"  ! 없음: {fname}")
            continue
        md = path.read_text(encoding="utf-8")
        r = Renderer(rn)
        rendered = r.render(md)
        total_secs += r.h2_count

        vid = f"vol-{rn}"
        body_html.append(
            f'<article class="vol" id="{vid}">'
            f'<div class="vol-tag"><span class="rn">권 {rn}</span>'
            f'<span class="ln"></span><span class="when">{esc(when)}</span></div>'
            f"{rendered}</article>")

        items = "".join(
            f'<a href="#{s["id"]}" class="{"l3" if s["l"] == 3 else ""}">{esc(s["t"])}</a>'
            for s in r.nav)
        nav_html.append(
            f'<div class="vgrp"><button class="vhead">'
            f'<span class="rn">{rn}</span>'
            f'<span>{esc(label)}<span class="desc">{esc(desc)}</span></span>'
            f'<span class="cnt">{r.h2_count}</span></button>'
            f'<div class="vbody"><a href="#{vid}">— 표지</a>{items}</div></div>')
        print(f"  · 권 {rn:<4} {label:<18} 섹션 {r.h2_count:>2} / 앵커 {len(r.nav):>3}")

    doc = f"""<!doctype html>
<html lang="ko" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SBTI 강사 가이드 · {BUILD_DATE}</title>
<meta name="description" content="SBTI 1·2·3 강사용 통합 가이드 — 에이전트, 멀티에이전트, 하네스 엔지니어링, MCP, 평가, 보안, 거버넌스, 운영">
<style>{CSS}</style>
</head>
<body>
<div id="prog"></div>
<button class="btn" id="menu">≡ 목차</button>

<aside id="rail">
  <div class="rail-head">
    <p class="brand">Instructor Briefing Dock</p>
    <h1>SBTI 1·2·3<br>강사 가이드</h1>
    <p class="meta">기준일 {BUILD_DATE}<br>120명 · 3일 · 59장</p>
  </div>
  <div class="search">
    <input id="q" type="search" placeholder="전체 검색 — 하네스, MCP, 87.5% …"
           autocomplete="off" spellcheck="false">
    <kbd>/</kbd>
  </div>
  <div id="hits"></div>
  <nav>{''.join(nav_html)}</nav>
  <div class="rail-foot">
    <button class="btn" id="theme">THEME</button>
    <button class="btn" onclick="window.print()">PRINT</button>
  </div>
</aside>

<main>
<div class="wrap">
  <header class="hero">
    <p class="kicker">Tech혁신Unit · 개발 AX Cell · 김지원</p>
    <h1>모델이 아니라<br><em>하네스</em>를 가르친다.</h1>
    <p class="sub">
      두 번의 독립 조사와 다섯 종의 운영 문서를 하나로 묶은 SBTI 1·2·3 강사용 레퍼런스.
      교차검증에서 갈린 지점과 강의 전 차단항목을 맨 앞에 두었다.
      강의 중에는 <code>/</code> 를 눌러 검색으로 쓴다.
    </p>
    <div class="facts">
      <div class="fact"><b>9</b><span>Volumes</span></div>
      <div class="fact"><b>{total_secs}</b><span>Sections</span></div>
      <div class="fact"><b>6</b><span>충돌 확정필요</span></div>
      <div class="fact"><b>15</b><span>P0 차단항목</span></div>
      <div class="fact"><b>{BUILD_DATE}</b><span>As of</span></div>
    </div>
  </header>
  {''.join(body_html)}
  <p class="tail">
    SBTI INSTRUCTOR GUIDE · BUILT {BUILD_DATE} · SELF-CONTAINED, NO NETWORK<br>
    SOURCE: guide/_source/data/*.md · REBUILD: python3 guide/build.py<br>
    내부 교육용. 사내 IP·경로·미확정 수치 포함 가능 — 외부 배포 전 마스킹·승인 필요.
  </p>
</div>
</main>

<button id="top" title="맨 위로">↑</button>
<script>{JS}</script>
</body>
</html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"\n  → {OUT}  ({len(doc.encode('utf-8')):,} bytes)")


if __name__ == "__main__":
    print("SBTI 강사 가이드 빌드")
    build()
