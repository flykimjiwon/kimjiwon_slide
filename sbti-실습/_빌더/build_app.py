#!/usr/bin/env python3
"""은행권_집계실습.html — 시난은행 집계 실습 단말 (디자인 A · 전산단말 스킨).

SQLite WASM 내장 · 완전 오프라인 · USB 더블클릭 실행.
흐름: 요청문 복사 → AI가 쿼리 작성 → 붙여넣고 실행＋채점(정답 자동 비교). 끝.
"""
import base64, io, os

SRC = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(SRC, 'node_modules/sql.js/dist')
OUT = '/Users/kimjiwon/Desktop/SBTI_PDF_모음_2026-08-05/08_은행권_집계실습/은행권_집계실습.html'

wasm_b64 = base64.b64encode(open(f'{D}/sql-wasm.wasm', 'rb').read()).decode()
loader = io.open(f'{D}/sql-wasm.js', encoding='utf-8').read().replace('</script>', '<\\/script>')
data_js = io.open(os.path.join(SRC, 'app_data.js'), encoding='utf-8').read()
ui_js = io.open(os.path.join(SRC, 'app_ui.js'), encoding='utf-8').read()

CSS = '''
:root{--navy:#1f3a5f;--navy2:#31548a;--line:#b6bcc5;--soft:#eef0f3;--bg:#e8eaed;
--txt:#1c2430;--mut:#5b6572;--ok:#2c7a3f;--warn:#b07f1e;--bad:#a83232;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
--font:"Malgun Gothic","맑은 고딕","돋움",Dotum,-apple-system,sans-serif}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;font-family:var(--font);background:var(--bg);color:var(--txt);
display:flex;flex-direction:column;overflow:hidden;font-size:13px}
.mono{font-family:var(--mono)}

/* 상단 바 */
.top{background:var(--navy);color:#fff;padding:8px 14px;display:flex;align-items:center;gap:10px;flex:none}
.top b{font-size:14.5px;letter-spacing:0}
.top .t{font-size:13px;color:#d7e0ee}
.top .id{margin-left:auto;font:400 11px var(--mono);color:#b9c8dd}
.top .fake{background:#7d1f1f;color:#ffd9d9;font-size:11px;font-weight:700;
padding:3px 10px;border:1px solid #a84444}

/* 탭 */
nav{background:#d5d9de;border-bottom:1px solid #9aa1ab;display:flex;flex:none}
nav button{appearance:none;background:#c8ccd2;border:0;border-right:1px solid #9aa1ab;
padding:8px 18px;font:700 12.5px var(--font);color:#3d4654;cursor:pointer}
nav button.on{background:#f4f5f7;color:#16202e;border-top:3px solid var(--navy);padding-top:5px}
nav button:hover:not(.on){background:#d0d4da}

main{flex:1;min-height:0;background:#f4f5f7}
.pane{display:none;height:100%;overflow:auto;padding:14px}
.pane.on{display:block}

/* 공통 박스 */
.box{background:#fff;border:1px solid var(--line)}
.boxh{background:var(--soft);border-bottom:1px solid var(--line);padding:7px 11px;
font-size:12.5px;font-weight:700;display:flex;gap:8px;align-items:center}
.boxh .code{color:var(--mut);font:400 11px var(--mono)}

/* 데이터 탭 */
.dwrap{display:grid;grid-template-columns:200px 1fr;gap:10px;height:100%;min-height:0}
.tlist{display:flex;flex-direction:column;gap:5px;overflow:auto}
.tlist button{background:#fff;border:1px solid var(--line);padding:8px 11px;text-align:left;
cursor:pointer;font:700 12.5px var(--font);display:flex;justify-content:space-between;
align-items:center;gap:6px;color:var(--txt)}
.tlist button small{font:400 10.5px var(--mono);color:var(--mut)}
.tlist button i{font-style:normal;font:400 11px var(--mono);color:var(--mut);white-space:nowrap}
.tlist button.on{border-color:var(--navy);border-left:4px solid var(--navy);background:#eef2f8}
.dview{background:#fff;border:1px solid var(--line);display:flex;flex-direction:column;min-height:0;overflow:hidden}
.dhead{padding:8px 12px 6px;font-size:12.5px;display:flex;align-items:center;gap:8px}
.dhead b{font:700 13px var(--mono)}
.dhead .r{margin-left:auto;color:var(--mut);font:400 11px var(--mono)}
.colbar{display:flex;flex-wrap:wrap;gap:4px;padding:0 12px 8px;border-bottom:1px solid var(--line)}
.colchip{background:var(--soft);border:1px solid #d5d9de;padding:3px 7px;font-size:11px;color:#3d4654}
.colchip b{font:700 11px var(--mono);color:var(--txt)}
.tag{display:inline-block;font:700 9px var(--mono);padding:0 4px;margin-left:4px;border:1px solid}
.tag.pk{color:var(--navy);border-color:#9db4d4;background:#e8eef7}
.tag.ix{color:var(--ok);border-color:#9cc7a7;background:#eaf5ed}
.tag.fk{color:var(--warn);border-color:#d9c08a;background:#f9f2df}
.dbody{flex:1;overflow:auto}

/* 결과 표 */
table.res{border-collapse:collapse;width:100%;font-size:12px}
table.res th,table.res td{border:1px solid #cfd4da;padding:4px 9px;text-align:left;white-space:nowrap}
table.res th{background:#dfe3e8;border-color:var(--line);position:sticky;top:0;font-weight:700;z-index:1}
table.res tbody tr:nth-child(even){background:#fafbfc}
table.res td.num{text-align:right;font-family:var(--mono)}
table.res td.null{color:#94a3b8;font-style:italic}
.msg{padding:12px 14px;font-size:12.5px;line-height:1.6}
.msg.err{color:var(--bad);font-family:var(--mono);white-space:pre-wrap;font-size:12px}
.msg.ok{color:var(--ok);font-weight:700}

/* 문제 탭 */
.probs{max-width:1020px;margin:0 auto}
.prob{background:#fff;border:1px solid var(--line);padding:0 0 12px}
.prob h3{margin:0;background:var(--soft);border-bottom:1px solid var(--line);
padding:8px 12px;font-size:13.5px;display:flex;align-items:center;gap:8px}
.prob .lv{font:700 10.5px var(--mono);color:var(--warn);border:1px solid #d9c08a;
background:#f9f2df;padding:1px 7px;margin-left:auto}
.prob .inner{padding:12px}
.prob .ask{font-size:12.5px;margin:0 0 10px;padding:9px 12px;background:var(--soft);
border-left:4px solid var(--navy);line-height:1.6}
.prob table.req{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:10px}
.prob table.req td{border:1px solid #d5d9de;padding:5px 9px;line-height:1.5}
.prob table.req td:first-child{background:var(--soft);width:74px;font-weight:700;text-align:center}
.steps3{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin:0 0 9px;font-size:12px;color:#3d4654}
.steps3 span{display:inline-flex;align-items:center;gap:5px}
.steps3 b{display:inline-grid;place-items:center;width:17px;height:17px;background:var(--navy);
color:#fff;font:700 10.5px var(--mono)}
.copied{font-size:12px;color:var(--ok);font-weight:700}
textarea{width:100%;height:170px;resize:vertical;border:1px solid var(--line);
padding:10px 12px;font:600 12.5px/1.65 var(--mono);background:#fff;outline:none;border-radius:0}
textarea:focus{border-color:var(--navy);box-shadow:inset 0 0 0 1px var(--navy)}
textarea::placeholder{color:#98a1ac}
.bar{display:flex;align-items:center;gap:6px;margin:8px 0}
button.run,button.ghost{border-radius:2px;cursor:pointer;font:700 12.5px var(--font);padding:7px 16px}
button.run{background:linear-gradient(#31548a,#1f3a5f);color:#fff;border:1px solid #162c47}
button.run:hover{background:linear-gradient(#3a5f99,#24446e)}
button.ghost{background:linear-gradient(#fdfdfd,#e4e7ea);border:1px solid #7b8494;color:var(--txt)}
.stat{margin-left:auto;font:400 11.5px var(--mono);color:var(--mut)}
.out{overflow:auto;border:1px solid var(--line);background:#fff}

/* 판정 */
.verdict{border:1px solid;padding:9px 12px;margin:6px 0;font-size:12.5px;line-height:1.6}
.verdict b{font-size:13px}
.verdict span{color:var(--mut);font:400 11.5px var(--mono);margin-left:6px}
.verdict.good{border-color:var(--ok);background:#eef7f0;color:#1d5c2e}
.verdict.bad{border-color:var(--bad);background:#fbeeee;color:#7c1f1f}
.verdict.warn{border-color:var(--warn);background:#fdf6e7;color:#7c5a10}
.verdict ul{margin:6px 0 0;padding-left:18px}
.verdict li{margin:3px 0}
.verdict .dh{font-weight:700;margin:8px 0 3px}
.verdict table.res th{position:static}
.verdict p{margin:5px 0 0}
.verdict p.mono{font-family:var(--mono);font-size:11.5px;white-space:pre-wrap}

details{border:1px solid var(--line);margin-top:10px;background:#fff}
details>summary{cursor:pointer;padding:8px 12px;font:700 12.5px var(--font);color:var(--navy);
list-style:none;background:var(--soft)}
details>summary::-webkit-details-marker{display:none}
details>summary:before{content:'[+] '}
details[open]>summary:before{content:'[-] '}
details .body{padding:10px 12px}
pre.sql{background:#10233c;color:#dbe6f5;padding:12px 14px;overflow-x:auto;
font:600 11.5px/1.6 var(--mono);margin:6px 0}
.trap{background:#fdf6e7;border:1px solid #d9c08a;padding:10px 12px;font-size:12px;
color:#6b4e0e;line-height:1.6;margin-top:6px}
.trap b{color:#513a06}

/* 자유 쿼리 */
.qwrap{max-width:1060px;margin:0 auto;display:flex;flex-direction:column;gap:7px;height:100%;min-height:0}
.chips{display:flex;flex-wrap:wrap;gap:5px}
.chips button{background:linear-gradient(#fdfdfd,#e4e7ea);border:1px solid #7b8494;
padding:5px 12px;font:700 11.5px var(--font);cursor:pointer;color:var(--txt);border-radius:2px}
.chips button:hover{background:#eef2f8;border-color:var(--navy);color:var(--navy)}
.qwrap textarea{height:140px}
.qwrap .out{flex:1;min-height:150px}
.loading{padding:40px;text-align:center;color:var(--mut);font-size:13px}
'''

HTML = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>시난은행 집계 실습 단말</title>
<style>{CSS}</style></head>
<body>
<div class="top">
  <b>시난은행</b><span class="t">집계 실습 단말</span>
  <span class="fake">가상 데이터 — 실존 은행·상품·직원과 무관</span>
  <span class="id">화면번호 SBT-0210 · 교육망 · 오프라인</span>
</div>
<nav>
  <button data-p="data" class="on">01 테이블조회</button>
  <button data-p="prob1">02 문제1 추천실적</button>
  <button data-p="prob2">03 문제2 페이지뷰</button>
  <button data-p="free">04 자유조회</button>
</nav>
<main>
  <div class="pane on" id="p-data"><div class="loading">데이터 적재 중…</div></div>
  <div class="pane" id="p-prob1"></div>
  <div class="pane" id="p-prob2"></div>
  <div class="pane" id="p-free"></div>
</main>
<script>
{loader}
</script>
<script>
var WASM_B64="{wasm_b64}";
{data_js}
{ui_js}
</script>
</body></html>
'''

io.open(OUT, 'w', encoding='utf-8').write(HTML)
print('은행권_집계실습.html', round(os.path.getsize(OUT) / 1024), 'KB')
