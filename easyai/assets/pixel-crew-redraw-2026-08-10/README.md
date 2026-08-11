# EASY AI Pixel Crew Redraw · 2026-08-10

EASY AI 본문에 있던 유령 삽화를 역할이 분명한 Pixel Crew로 다시 그린 교체 팩이다.
본문 채택본 11점과 그래프 엔지니어링 확장 후보 4점을 모두 1672×941 가로 PNG로 보관한다.

## 공통 시각 규칙

- 배경: `#101722` 남색 캔버스 + `#123166` 사각 도트 격자
- 신호선: `#18d7f2`, 제어 코어: `#1677ff`
- 크루: 흰 사각 눈, 검은 사각 동공, 분홍 사각 볼, 세 갈래 블록 발
- 역할: 청록 설계자, 노랑 빌더, 코랄 검증자, 보라 리서처, 초록 기록·운영자
- 역할 소품: 스카프·가방, 안전모·렌치, 삼각자·체크리스트, 돋보기·노트, 문서 가방
- 금지: 이미지 안 텍스트·로고·워터마크, 미로·펠릿·PAC-MAN 참조, 일반 유령 실루엣

## 본문 채택본

| 순서 | 파일 | 교체 장면 |
| --- | --- | --- |
| 1 | `01-cover-pixel-crew.png` | 표지 설계 브리핑 |
| 2 | `02-context-window-pixel-crew.png` | 컨텍스트 윈도우와 용량 한계 |
| 3 | `03-grounding-pixel-crew.png` | 근거 검증과 출처 선별 |
| 4 | `04-multiagent-pixel-crew.png` | 멀티에이전트 위임·회수 |
| 5 | `05-mcp-a2a-pixel-crew.png` | 도구 연결과 전문 에이전트 릴레이 |
| 6 | `06-rag-search-pixel-crew.png` | RAG 검색·근거 답변 |
| 7 | `07-memory-wiki-pixel-crew.png` | 검색·검증·위키 적재 |
| 8 | `08-context-compaction-pixel-crew.png` | 컨텍스트 압축 |
| 9 | `09-loop-harness-pixel-crew.png` | 계획·승인·실행·관측·피드백 루프 |
| 10 | `10-loop-repair-pixel-crew.png` | 목표·구현·검증·실패 수리·완료 루프 |
| 11 | `11-prompt-optimization-pixel-crew.png` | 프롬프트 후보 평가·탈락·재작성·최종 선택 |

`embed-into-easyai.mjs`를 저장소 루트에서 실행하면 위 11점을 `easyai/index.html`의
`ghost-cover` 1곳, `ghost-visual` 8곳, 루프 장의 `surface-card` 2곳에 순서대로 PNG data URI로 임베드한다.

## 그래프 엔지니어링 확장 후보

| 파일 | 장면 |
| --- | --- |
| `graph-01-system-map.png` | 전체 노드·엣지·승인·실패 회귀 노선도 |
| `graph-02-fanout-join.png` | 세 작업의 병렬 fan-out과 단일 join |
| `graph-03-human-checkpoint.png` | 사람 승인, 반려 루프, 상태 체크포인트 |
| `graph-04-failure-routing-state.png` | 실패 원인별 분기, 공유 상태, 재합류 |

## 생성 기록

- 생성일: 2026-08-10
- 생성 방식: Codex built-in image generation
- 로컬 참조: 기존 EASY AI 본문 삽화, 이 팩의 표지 앵커, 멀티에이전트·루프 채택본
- 사람 담당: 콘셉트 제공, 역할 정의, 선별 및 교재 반영 김지원
- 생성 도구 담당: 장면 재구성 및 픽셀 삽화 생성 보조
- 원본 생성 결과는 Codex 생성 이미지 보관소에 남기고, 프로젝트 소비본을 이 폴더에 복사했다.
