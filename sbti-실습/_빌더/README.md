# 빌더 소스 (재생성용)

- `build_app.py` + `app_data.js` + `app_ui.js` → `08.../은행권_집계실습.html` 생성
  - sql.js(SQLite WASM) dist 경로와 출력 경로가 하드코딩돼 있으니 실행 전 수정 필요
  - `npm i sql.js` 후 `node_modules/sql.js/dist` 를 참조한다
- `gen_bank.py` → 08 의 schema/문제/정답/보고서(PostgreSQL 정본) 생성
- `gen_practice.py` → 06 roombook 탐색 과제 생성
- `gen_sql.py` → 07 SQL 튜닝 전/후 세트 생성
