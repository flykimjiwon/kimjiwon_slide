# EASY AI 정본 픽셀 삽화 팩

생성일: 2026-08-03
상태: **확장 정본** — 라이브 [`/sbti4`](https://kimjiwon-slide.vercel.app/sbti4) 표지의 그림체를 기준으로 만든 30개 개념 · 90점. 기존 27점은 유지하고 2026-08-04에 18개 개념 · 54점과, 원본 개념을 다시 해석한 픽셀크루 3개 개념 · 9점을 보강했다.

[정본 갤러리 열기](index.html) · [이전 후보 팩 보존본](../expansion-2026-08/index.html)

## 기준 그림체

- `#101722` 평면 남색 위의 큰 `#123166` 사각 도트 격자
- 큰 단위의 정사각 픽셀, 계단형 머리·흰 사각 눈·세 갈래 발을 가진 친근한 유령 작업자
- 청록 직각 신호선과 파란 동심 사각 제어 코어, 노랑 헬멧·도구와 절제된 초록 도구 포인트
- 텍스트·숫자·브랜드·로고·워터마크 없음
- 유광 3D, 부드러운 모서리, 에어브러시, 글로우 남용, 미세 노이즈 금지

## 규격

| Variant | Final pixel size | Use |
| --- | --- | --- |
| `wide` | 1672 × 941 · 16:9 | 장 도입·넓은 본문 figure |
| `square` | 941 × 941 · 1:1 | 요약 카드·사이드 미디어 |
| `portrait` | 753 × 941 · 4:5 | 좁은 열·모바일·세로 포스터 |

## 개념

| # | Concept | Files |
| --- | --- | --- |
| 01 | 토큰 · 컨텍스트 윈도우 | `01-context-window-{wide,square,portrait}.png` |
| 02 | 그라운딩 vs 환각 | `02-grounding-{wide,square,portrait}.png` |
| 03 | 에이전틱 루프 | `03-agentic-loop-{wide,square,portrait}.png` |
| 04 | 도구 호출 · MCP | `04-tool-calling-mcp-{wide,square,portrait}.png` |
| 05 | 하네스 · 가드레일 | `05-harness-guardrails-{wide,square,portrait}.png` |
| 06 | 멀티에이전트 핸드오프 | `06-multiagent-handoff-{wide,square,portrait}.png` |
| 07 | RAG와 에이전틱 검색 | `07-rag-agentic-search-{wide,square,portrait}.png` |
| 08 | 컨텍스트 부패 · 압축 | `08-context-compaction-{wide,square,portrait}.png` |
| 09 | 메모리 · 스킬 · 규칙 · 위키 | `09-memory-wiki-{wide,square,portrait}.png` |
| 10 | MCP 서버 조립 | `10-mcp-server-kit-{wide,square,portrait}.png` |
| 11 | MCP 프리미티브 | `11-mcp-primitives-{wide,square,portrait}.png` |
| 12 | MCP 전송 · 세션 | `12-mcp-transport-session-{wide,square,portrait}.png` |
| 13 | A2A 에이전트 카드 | `13-a2a-agent-card-{wide,square,portrait}.png` |
| 14 | 권한 · 인증 · 동의 | `14-auth-permissions-{wide,square,portrait}.png` |
| 15 | 스키마 · 구조화 출력 | `15-structured-output-{wide,square,portrait}.png` |
| 16 | 재시도 · 오류 복구 | `16-retry-recovery-{wide,square,portrait}.png` |
| 17 | 스트리밍 · 진행 신호 | `17-streaming-progress-{wide,square,portrait}.png` |
| 18 | 플래너 · 라우터 | `18-planner-router-{wide,square,portrait}.png` |
| 19 | 서브에이전트 트리 | `19-subagent-tree-{wide,square,portrait}.png` |
| 20 | 사람 검토 · 승인 | `20-human-approval-{wide,square,portrait}.png` |
| 21 | 평가 · 테스트 하네스 | `21-eval-test-harness-{wide,square,portrait}.png` |
| 22 | 트레이스 · 관찰성 | `22-traces-observability-{wide,square,portrait}.png` |
| 23 | 샌드박스 · 격리 | `23-sandbox-isolation-{wide,square,portrait}.png` |
| 24 | 청킹 · 벡터 인덱스 | `24-chunking-vector-index-{wide,square,portrait}.png` |
| 25 | 의미 기반 모델 라우터 | `25-semantic-model-router-{wide,square,portrait}.png` |
| 26 | 컨텍스트 캐시 | `26-context-cache-{wide,square,portrait}.png` |
| 27 | 메모리 수명주기 | `27-memory-lifecycle-{wide,square,portrait}.png` |
| 28 | 픽셀크루 브리핑 | `28-pixel-crew-briefing-{wide,square,portrait}.png` |
| 29 | MCP · A2A 픽셀크루 릴레이 | `29-pixel-crew-mcp-a2a-relay-{wide,square,portrait}.png` |
| 30 | 하네스 픽셀크루 게이트 | `30-pixel-crew-harness-gates-{wide,square,portrait}.png` |

## 채택 규칙

1. 슬라이드 한 지점에는 우선 한 장만 배치해 교육 밀도를 유지한다.
2. 최종 채택 시 오프라인 단일 HTML의 data URI, `alt`, `figcaption`을 함께 업데이트한다.
3. 기존 27점은 이 폴더에 그대로 보존한다. 새 28–30번은 본문 원본을 덮어쓰지 않는 픽셀크루 재해석 후보이며, 이전 [`expansion-2026-08`](../expansion-2026-08/) 후보와 현재 본문 삽화도 변경하지 않는다.

## 제작 방식

초기 장면 원본을 바탕으로, 라이브 표지·프로젝트 SVG에서 추출한 픽셀 문법을 기준으로 전 27점을 하드 픽셀로 재렌더링했다. 모든 출력은 단색 채움·사각 도형만 사용하며, 정사각/세로 출력은 이 폴더의 최종 캔버스 규격으로 별도 구성했다.
