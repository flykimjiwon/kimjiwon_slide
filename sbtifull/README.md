# sbtifull — S.B.T.I 강의 3부작 공개본 (모자이크)

외부(링크드인 등) 공유용 통합 덱이다. `sbti1/` `sbti2/` `sbti3/` 원본에서 **생성된 사본**이며,
원본은 이 폴더의 어떤 스크립트도 수정하지 않는다.

| | 주소 |
|---|---|
| 공개본 통합 뷰어 | `/sbtifull` |
| 원본 ↔ 공개본 대조 (내부 검수용) | `/sbtifull/compare` |
| EASY AI 용어사전 (원본 그대로 사용) | `/easyai` |

## 왜 새로 만들었나

원본 `sbti2`는 실명·부서명을 CSS `filter:blur(4px)` 45곳으로 가리고 있었다.
**blur는 화면에서만 흐릴 뿐 HTML 소스에는 원문이 그대로 남는다.** 소스 보기나 개발자도구로 바로 읽힌다.
공개본은 문자열 자체를 치환하고 blur 필터를 걷어냈다.

## 무엇을 바꿨나

- **실명 20명** → `참여자 A`~`참여자 T`
- **부서 실명 31종** → `서비스 개발 1부` 등 일반화
- **회사·내부 시스템** → 신한은행 → `금융권 A사`, GITSOP → `사내 형상관리 시스템`, 스윙 SSO → `사내 SSO`, 행내 → `사내`, 땡겨요 → `자체 플랫폼 서비스`
- **제품명** → 택가이코드 → `사내 AI 코딩 도구`, TECHAI CODE → `AI CODING TOOL` (사용자 결정: 사내 도구 익명화)
- **이미지 4장 마스킹** (불투명 사각형 — 복원 불가): `tweb_admin.png` `tweb_chat.png` `tgc_devreq_aicr.png` `tgc_wiki_mcp_ask.png`
- **이미지·영상 4개 제외**: `techai_website_landing.png` `ttaengyo_logo.png` `ttaeng_poc_poster.jpg` `ttaeng_poc_captioned.mp4`

전체 대조표는 `/sbtifull/compare` 에 있다.

## 재생성

```bash
cd my-projects/kimjiwon_slide
python3 scripts/build_sbtifull.py          # 문자열 치환 + 덱 폴더 재생성
python3 scripts/redact_sbtifull_assets.py  # 이미지 마스킹·제외 (반드시 위 스크립트 다음)
```

`build_sbtifull.py` 는 덱 폴더(`sbti1~3/`)만 갈아엎고 `index.html` · `compare.html` · 이 README는 건드리지 않는다.
치환 규칙은 스크립트 상단의 `NAME_MAP` / `DEPT_MAP` / `ORG_MAP` / `PRODUCT_MAP` 에 있다.

검증은 빌드 시 자동으로 돈다 — 금칙어 55종을 재검색해 0건이어야 통과한다. 결과는 `_build_report.json`.

## 아직 남은 것

- **원본 `/sbti1` `/sbti2` `/sbti3` 는 여전히 공개 접근된다.** 비밀번호 보호를 걸기 전까지 원본 실명이 소스에 노출된 상태다.
- 터미널·VS Code 캡처 약 25장에 제품 워드마크나 `.tgc` 경로가 남아 있을 수 있다. 회사 식별자는 아니지만 익명화 방침과는 어긋난다.
- 집계 수치(사용자 2,018명 · 주간 34.9억 토큰 · API Key 465건)는 그대로 뒀다. 부서명을 익명화해 특정은 어렵지만 공개 여부는 판단이 필요하다.
