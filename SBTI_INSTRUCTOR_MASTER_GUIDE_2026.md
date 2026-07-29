# SBTI 1·2·3 강사 마스터 가이드

조사 기준일: 2026-07-29 KST  
대상 자료: `sbti1`, `sbti2`, `sbti3`  
목적: 강사가 3일 과정에서 모델, LLM, 에이전트, 멀티에이전트, 코딩 에이전트, 하네스 엔지니어링, 평가, 보안, 거버넌스를 정확히 설명하고 실습을 운영할 수 있게 하는 것

## 0. 결론

현재 자료는 15장 + 31장 + 13장, 총 59장이다. 흐름은 좋다.

> 시장과 기본 개념 → TECHAI Code와 에이전트 구조 → 사내 프레임워크와 MCP 적용

그러나 현재 형태는 3일짜리 역량 과정이라기보다 완성도 높은 내부 제품 브리핑에 가깝다. 강의 전에 아래 다섯 가지를 반드시 보강해야 한다.

1. 제품 설명보다 먼저 `모델 → 컨텍스트 → 하네스 → 도구/환경 → 증거 → 사람/정책`의 계층을 가르친다.
2. 세 날 모두 참가자가 직접 남기는 결과물과 판정 기준을 만든다.
3. 도구 수, 버전, 모델, MCP, 권한, 로그, 성과 수치를 하나의 강의용 릴리스 매니페스트로 고정한다.
4. 멀티에이전트와 장기 자율실행은 장점보다 적용 조건, 비용, 충돌, 중단, 복구를 함께 가르친다.
5. 공개 벤치마크와 벤더 발표를 업무 생산성 또는 사내 제품 우위의 증거로 사용하지 않는다.

강사가 가장 먼저 외워야 할 문장은 다음과 같다.

> 에이전트의 성능은 모델 하나의 성능이 아니다. 모델, 컨텍스트, 하네스, 도구, 실행환경, 권한, 검증, 사람의 결합 성능이다.

## 1. 강의 전에 즉시 처리할 차단 항목

| 우선순위 | 현재 상태 | 강의 전 조치 |
|---|---|---|
| P0 | `baedal-ten.vercel.app`, `slide-agentmake.vercel.app`가 2026-07-29 기준 HTTP 404 | 로컬 HTML·동영상 fallback으로 링크 교체 |
| P0 | 도구 수가 13, 14, 37, 50+로 충돌 | 정확한 강의 빌드의 `/tools/catalog` 결과만 사용 |
| P0 | VSIX는 `0.1.107`, 내장 서버는 `tgc-server dev`, 포함 가이드는 `0.1.62` 표기 | VSIX 해시, 서버 빌드 ID, 모델, 권한, MCP를 릴리스 매니페스트에 고정 |
| P0 | Day 3의 권한 설명과 실제 autopilot 정책이 다름 | `allow/ask/deny`와 autopilot 예외를 실제 빌드로 시연 |
| P0 | Wiki/ProFrame MCP의 기본 탑재·자동 최신화·실사용 주장이 빌드별 문서와 충돌 | owner, prod endpoint, build ID, entitlement, 갱신·rollback 증거 없으면 “환경별 데모”로 하향 |
| P0 | 사용자·WAU·키·요청·토큰·절감·87.5% 수치의 원자료가 없음 | 근거 카드가 완성되지 않으면 삭제하거나 “내부 POC 최대값/시나리오 추정”으로 제한 |
| P0 | “문서 즉시 학습”이 weight training처럼 들림 | “파싱·검색·컨텍스트 주입”으로 수정 |
| P1 | Day 3가 가장 실무적인데 직접 실습이 없음 | 제한된 프레임워크 변경 capstone 추가 |
| P1 | presenter note가 슬라이드 반복 수준 | 시간, 질문, 예상답, 실패 대응, 전환 문장 추가 |

### 확인된 강의 후보 artifact

- VS Code release bundle: [`vscode-v0.1.107`](/Users/jiwonkim/Desktop/kimjiwon/techai/택가이코드/releases/vscode-v0.1.107)
- Ttaengyo POC 로컬 앱: [`baedal/app`](/Users/jiwonkim/Desktop/kimjiwon/my-projects/baedal/app)
- Ttaengyo POC 대체 영상: [`ttaeng_poc_captioned_gitsop_removed_7m51.mp4`](/Users/jiwonkim/Desktop/kimjiwon/my-projects/baedal/demo-video/out/ttaeng_poc_captioned_gitsop_removed_7m51.mp4)
- Agent Builder 대체 HTML: [`AGENT_BUILDER_TALK_V2_LIGHT_2026-06-08.html`](/Users/jiwonkim/Desktop/kimjiwon/_career_doc/presentation-archive/AGENT_BUILDER_TALK_V2_LIGHT_2026-06-08.html)

## 2. 강의 전체를 관통할 시스템 모델

```text
업무 목표·완료 기준
        ↓
모델: 해석·추론·선택·생성
        ↓
컨텍스트: 지시·코드·문서·상태·기억
        ↓
하네스: 루프·도구·권한·예산·복구·검증·관측
        ↓
실행환경: 파일·터미널·브라우저·IDE·컨테이너·네트워크
        ↓
증거: diff·테스트·빌드·로그·스크린샷·trace·평가
        ↓
사람과 조직: 승인·책임·정책·감사·배포
```

이 계층을 섞으면 다음과 같은 잘못된 설명이 나온다.

- 모델이 파일을 수정했다: 실제로는 하네스가 모델의 요청을 도구 호출로 실행했다.
- 모델이 사내 문서를 학습했다: 실제로는 문서를 검색해 현재 컨텍스트에 넣었을 수 있다.
- MCP가 안전하다: MCP는 통신 규약이며 신뢰·권한·감사는 별도 통제다.
- 멀티에이전트가 더 똑똑하다: 병렬화와 관점 다양성은 늘 수 있지만 오류 상관, 비용, 충돌도 늘어난다.
- JSON Schema를 쓰면 정확하다: 형식 오류는 줄지만 의미적 진실, 권한, 업무 적합성은 보장하지 않는다.
- 벤치마크 80점 모델이 우리 업무에서도 80점이다: 과제, 하네스, 도구, 예산, 채점이 다르면 점수는 이식되지 않는다.

## 3. 모델과 LLM: 강사가 설명할 최소 깊이

### 3.1 안정적으로 알아야 할 개념

- `foundation model`: 다양한 하위 업무에 적응하는 범용 사전학습 모델
- `LLM`: 언어와 코드의 token sequence를 다루는 대규모 모델
- `multimodal model`: 텍스트 외 이미지, 음성, 영상, UI 상태 등을 함께 다루는 모델
- `token`: 모델이 처리하는 기본 단위. 문자나 단어와 정확히 일치하지 않는다.
- `embedding`: 텍스트·이미지 등을 의미 공간의 vector로 표현한 값
- `Transformer`: attention으로 sequence 안의 관계를 계산하는 기본 구조
- `pretraining`: 대규모 데이터에서 일반 패턴을 학습
- `post-training`: instruction following, preference, safety, tool use를 강화
- `inference`: 학습된 weight로 실제 응답을 생성하는 과정
- `reasoning effort/test-time compute`: 한 요청에 더 많은 탐색·계산을 투입하는 운영 설정
- `MoE`: 일부 expert만 선택적으로 활성화해 계산 효율을 얻는 구조
- `distillation`: 큰 모델의 행동을 작은 모델에 전달
- `quantization`: weight 표현 정밀도를 낮춰 메모리·속도 비용을 줄임
- `fine-tuning/LoRA`: 특정 업무나 행동 양식을 weight에 반영
- `RAG`: 외부 지식을 검색해 현재 요청의 근거로 제공

### 3.2 2026 모델 트렌드

1. 하나의 “최고 모델”보다 작업·가격·속도에 따른 family와 routing이 일반화됐다.
2. reasoning은 고정된 별도 모델 종류가 아니라 effort, budget, tool loop와 함께 운영된다.
3. coding, browser, computer use, document work가 모델 발표의 핵심 평가 축이 됐다.
4. 긴 컨텍스트와 prompt cache가 확대됐지만 relevant context를 고르는 문제는 사라지지 않았다.
5. open-weight 모델의 비용·배포 선택지가 넓어졌지만 라이선스와 완전한 재현 가능성은 별개다.
6. 모델 발표 점수보다 독립 평가, harness recipe, 비용, latency, 거부율, 안전성을 함께 봐야 한다.

### 3.3 2026-07-29 기준 대표 모델 지도

| 공급자 | 현재 대표 계열 | 강의에서 강조할 점 | 주의 |
|---|---|---|---|
| OpenAI | GPT-5.6 Sol, Terra, Luna | effort·비용 tier, tool use, coding, multi-agent beta | 제품 발표 점수와 독립 평가를 분리 |
| Anthropic | Claude Sonnet 5, Opus 4.8 계열 | long-running coding, context engineering, agent harness | 모델별 비용은 출력량과 harness에 크게 좌우 |
| Google | Gemini 3.5, Gemini 3.6 Flash | multimodal, action, 빠른 효율 tier | 공개적으로 확인된 3.6은 Flash이며 Pro로 확대 해석 금지 |
| Meta | Llama 4 계열 | open-weight 배포와 생태계 | Llama 라이선스를 OSI open source로 부르면 안 됨 |
| Alibaba/Qwen | Qwen3.5, Qwen3.6 | open-weight 효율과 coding | 공식 점수 재현에 tool/harness recipe 영향이 큼 |
| DeepSeek | DeepSeek V4/V4 Pro | 1M context, 가격 효율, 공개 model card/report | 독립 NIST 비교는 blanket frontier parity를 지지하지 않음 |
| Mistral | Mistral Small 4 계열 | 작은 배포 모델과 유럽 생태계 | 정확한 배포·라이선스 조건을 모델별 확인 |

현재 모델에 대한 가장 안전한 설명:

> GPT-5.6 Sol은 최신 broad benchmark에서 강하지만 장기 자율성은 평가 방법에 따라 크게 흔들린다. Sonnet 5는 강한 경쟁 모델이지만 보편적 cost-quality 1위라고 할 수 없다. Gemini 3.6 Flash는 품질 도약보다 속도·효율 개선의 증거가 강하다. Qwen과 DeepSeek은 open-weight 비용 효율이 매력적이지만 모든 과제에서 proprietary frontier와 동급이라는 증거는 없다.

### 3.4 open source라는 말의 정확한 구분

- `open source AI`: OSI Open Source AI Definition이 요구하는 수정·재현·사용에 필요한 구성요소와 권리가 충족되는 범주
- `open model`: 공개 접근 모델이라는 느슨한 표현
- `open weights`: weight 파일을 받을 수 있다는 뜻
- `source-available`: 일부 source나 weight는 공개하되 사용 제약이 존재

따라서 “weight를 받을 수 있다 = open source”는 틀린 설명이다. 라이선스, 학습 정보, 코드, 데이터 정보, 수정·재배포 권리를 따로 확인한다.

## 4. 에이전트와 workflow

### 4.1 operational definition

`workflow`는 사람이 미리 정한 경로를 실행한다. `agent`는 목표와 제약 안에서 모델이 다음 도구, 순서, 분기, 재시도, 중단 중 일부를 동적으로 결정한다.

```text
목표 수신
→ 상태 관찰
→ 다음 행동 결정
→ 도구 실행
→ 결과 관찰
→ 완료·계속·복구·에스컬레이션 판단
```

에이전트를 단순히 “LLM이 여러 번 대답하는 것”으로 가르치면 안 된다. 상태, 도구, 부작용, 권한, 종료조건이 있어야 시스템 관점의 에이전트를 설명할 수 있다.

### 4.2 workflow가 더 나은 경우

- 경로와 규칙이 이미 알려져 있음
- 규정·감사·재현성이 중요함
- 실패 비용이 큼
- 입력·출력 schema가 안정적임
- 예외를 코드로 처리할 수 있음

### 4.3 agent가 유리할 수 있는 경우

- 저장소나 자료를 먼저 탐색해야 함
- 문제 분해와 도구 선택이 업무의 핵심임
- 정해진 경로가 없고 피드백을 보며 수정해야 함
- 사람이 모든 분기를 작성하는 비용이 큼
- 중간 상태를 관찰해 복구할 수 있음

### 4.4 대표 패턴

| 패턴 | 용도 | 주요 위험 |
|---|---|---|
| Prompt chaining | 단계별 변환 | 앞 단계 오류 전파 |
| Routing | 업무별 모델·도구 선택 | 잘못된 분류 |
| Parallelization | 독립 조사·검사 | 중복 비용·합성 오류 |
| ReAct | 추론과 행동 반복 | 무한 루프·도구 오용 |
| Plan-and-execute | 큰 과업의 계획·실행 분리 | stale plan |
| Evaluator-optimizer | 생성과 비평 반복 | 같은 모델의 상관 오류 |
| Supervisor-worker | 관리자가 하위 작업 배분 | 병목·권한 확대 |
| Agent-as-tool | 상위 agent가 전문 agent 호출 | 결과 신뢰 과잉 |
| Handoff | 다른 agent가 소유권 인수 | 목표·상태 손실 |
| Human-in-the-loop | 승인·판단을 사람에게 요청 | 승인 피로·자동 동의 |

### 4.5 computer use

컴퓨터 사용 agent는 화면을 보고 마우스·키보드를 조작한다. 구조화 API나 안정된 browser automation보다 느리고 깨지기 쉬우며 화면 prompt injection의 영향을 받는다. 우선순위는 보통 다음과 같다.

```text
직접 API > typed tool > DOM/browser automation > 화면 기반 computer use
```

computer use는 마지막 호환성 경로로 가르친다.

## 5. 멀티에이전트

### 5.1 언제 쓸 것인가

- 서로 독립적인 자료를 병렬 조사
- 보안, 품질, 요구사항처럼 다른 관점의 review
- 서로 다른 권한·도메인을 격리
- 긴 작업의 context를 역할별로 분리
- 동일 답을 복제하는 것이 아니라 서로 다른 증거를 생산

### 5.2 언제 쓰지 말 것인가

- 한 agent가 짧게 끝낼 수 있음
- 같은 파일을 동시에 수정해야 함
- 작업 경계와 통합 owner가 없음
- 결과를 검증할 수 없음
- token·latency·운영 복잡성이 이익보다 큼
- 동일 모델·동일 prompt의 다수결만 수행

### 5.3 topology

- `manager-workers`: manager가 작업을 분해하고 합성
- `peer-to-peer`: agent끼리 메시지와 artifact 교환
- `blackboard`: 공용 상태에 결과를 기록
- `pipeline`: specialist가 순서대로 인계
- `debate/critic`: 생성자와 비평자 분리
- `map-reduce`: 병렬 탐색 후 중앙 합성
- `hierarchical`: 여러 manager와 worker 계층

### 5.4 운영 규칙

1. 한 task에는 한 owner를 둔다.
2. 쓰기 workspace는 worktree, branch, container로 격리한다.
3. DAG와 dependency를 명시한다.
4. parent가 통합, 충돌, 최종 검증을 소유한다.
5. time, token, turn, recursion, concurrency budget을 둔다.
6. 하위 agent 결과를 비신뢰 입력으로 취급한다.
7. agent가 멈춘 것을 완료로 보지 말고 acceptance evidence를 확인한다.

### 5.5 강의에서 할 비교 실험

동일한 저장소 탐색 문제를 다음 세 방식으로 실행하고 표를 채운다.

| 방식 | 성공 | 벽시계 시간 | token/cost | 중복 | 오류 | 사람이 검토한 시간 |
|---|---:|---:|---:|---:|---:|---:|
| 단일 agent | | | | | | |
| 3-agent 병렬 탐색 | | | | | | |
| workflow + 1 review agent | | | | | | |

이 실험의 목적은 멀티에이전트를 홍보하는 것이 아니라 어떤 조건에서 실제로 이득인지 판단하는 것이다.

## 6. Prompt, context, RAG, memory, skill

### 6.1 범위 차이

- `prompt engineering`: 요청과 지시를 쓰는 기술
- `context engineering`: 목표 달성에 필요한 정보와 상태를 선택·배치·갱신하는 기술
- `harness engineering`: context를 포함해 실행 루프, 도구, 환경, 권한, 검증, 관측을 설계하는 기술
- `platform engineering`: 여러 팀이 안전하게 사용할 공통 실행·배포·개발 기반

### 6.2 긴 context가 RAG를 대체하지 않는 이유

| 기법 | 해결하는 문제 |
|---|---|
| Long context | 한 요청이 볼 수 있는 최대 범위 |
| RAG | 필요한 자료를 찾고 근거로 제공 |
| Memory | 세션을 넘어 선택된 상태를 유지 |
| Prompt cache/KV cache | 반복 입력의 계산 비용과 latency 절감 |
| Compaction | 오래된 실행 상태를 압축해 다음 context로 전달 |

긴 context도 relevance, freshness, 권한 filtering, 출처, lost-in-the-middle, context rot 문제를 해결하지 않는다. 실무에서는 hybrid가 일반적이다.

### 6.3 RAG pipeline

```text
source ownership
→ 수집·파싱
→ 정제·PII/secret 처리
→ chunking·metadata·ACL
→ index
→ query rewrite
→ sparse/dense hybrid retrieval
→ rerank
→ context assembly
→ cited answer
→ retrieval/answer evaluation
→ 갱신·삭제·감사
```

RAG 품질은 “답이 좋아 보인다”로 평가하지 않는다.

- 검색: recall@k, precision@k, MRR, nDCG, 권한 위반 0
- 답변: citation correctness, groundedness, completeness, abstention
- 운영: freshness, latency, cost, 삭제 반영 시간, owner coverage

### 6.4 memory lifecycle

- `working memory`: 현재 실행의 임시 상태
- `episodic memory`: 과거 작업과 사건
- `semantic memory`: 일반화된 사실
- `procedural memory`: 반복 절차
- `environment state`: 파일, branch, issue, 실행 결과
- `experience memory`: 성공·실패에서 추출한 교훈

전체 chat를 영구 저장하는 것은 memory design이 아니다. 저장할 항목을 선택하고, source·version·owner·expiry·delete policy를 붙이며, 사용자와 업무 권한을 보존해야 한다.

### 6.5 knowledge, memory, skill, rule

- `knowledge`: 현재 업무가 참조할 사실
- `memory`: 여러 실행 사이에 지속되는 선택된 상태
- `skill`: 반복 가능한 절차와 필요한 artifact
- `rule`: 허용·금지·승인·품질 기준
- `tool`: 환경에서 실제 행동을 수행하는 capability

Agent Skills의 `SKILL.md`는 절차를 progressive disclosure 방식으로 제공할 수 있지만, `allowed-tools` 같은 필드도 제품별 지원과 실제 권한 강제를 따로 확인해야 한다.

## 7. Agent protocol stack

| 계층 | 프로토콜·규약 | 주 연결 | 표준화 범위 | 보장하지 않는 것 |
|---|---|---|---|---|
| 모델 호출 | Function calling, structured output, Responses | model ↔ host | tool schema·event·output 형식 | tool 신뢰·업무 권한 |
| 도구·데이터 | MCP | AI host/client ↔ server | tools, resources, prompts와 호출 | server 신뢰·최소권한·injection 방어 |
| Agent 간 | A2A | agent client ↔ opaque agent server | Agent Card, message, task, artifact, stream | 내부 subagent·tool policy·업무 승인 |
| Agent UI | AG-UI | frontend ↔ agent backend | event, state, interrupt, streaming UI | backend 보안·agent 신뢰 |
| Coding client | ACP | editor/IDE ↔ coding agent | session, plan, diff, permission UX | agent 내부·sandbox·조직 authorization |
| 절차 package | Agent Skills | agent ↔ procedural package | `SKILL.md`, scripts, references, assets | script 안전성·조직 승인 |
| 코드 의미 | LSP | editor/agent ↔ language server | symbol, diagnostic, definition, reference | 업무 요구사항·runtime correctness |
| 관측 | OpenTelemetry | runtime ↔ observability backend | trace, metric, log convention | 자동적인 원인 분석·개인정보 적법성 |

일반 조합:

```text
IDE --ACP--> coding agent --MCP--> repository/database/tool
                         \
                          --A2A--> independent remote agent
frontend --AG-UI--------/
```

프로토콜을 조합할 수 있다는 것은 안전 정책, identity, authorization, audit가 전이된다는 뜻이 아니다. hop마다 principal, credential scope, approval, context filtering, audit, timeout, revocation을 다시 결정한다.

### 7.1 MCP 2026-07-28

2026-07-28 revision은 사소한 추가판이 아니라 `initialize` 제거, `server/discover`, 요청별 metadata와 capability negotiation 등 구조가 바뀐 새 protocol era다.

2026-07-29의 정확한 채택 상태:

- Go `v1.7.0`, Python `v2.0.0`, C# `v2.0.0`, Rust `rmcp-v3.0.0`은 modern wire를 지원
- TypeScript v2 package는 modern negotiation을 명시적으로 opt-in해야 함
- Java v2는 `2025-11-25`를 추적
- 주요 VS Code, Copilot, Claude, Codex 제품이 실제 협상한 wire version은 공개 문서에서 확인되지 않음
- conformance infrastructure는 아직 alpha version

따라서 “MCP 최신판으로 모두 전환됐다”가 아니라 다음처럼 말한다.

> 안정 SDK는 출시됐지만 생태계는 modern/legacy dual-wire 상태다. 서버와 client의 실제 negotiated version을 trace에서 확인해야 한다.

### 7.2 A2A와 AG-UI 성숙도

- A2A: v1.0 stable, normative version header, JSON-RPC/gRPC/HTTP+JSON, TCK·ITK, Linux Foundation governance. 다만 SDK 동기화와 federated registry는 미완성.
- AG-UI: adapter와 실제 사용은 넓지만 core가 pre-1.0이고 공개 formal TCK·certification·version negotiation은 확인되지 않음.
- ACP: v1 stable, v2 draft. editor와 coding agent를 분리한다. remote agent 지원은 발전 중.

## 8. 하네스 엔지니어링

### 8.1 정확한 정의

> Agent harness는 foundation model을 제외하고, agent가 무엇을 관찰하고 기억하며 호출하고 수정할 수 있는지, 어떤 피드백을 받고 무엇을 증명해야 완료되는지를 중재하는 runtime/control system이다.

> Harness engineering은 그 runtime과 control을 설계, versioning, 운영, 측정, 개선하는 지속적 engineering discipline이다.

“하네스 엔지니어링”이라는 표현의 최초 창안자를 단정할 근거는 없다. OpenAI와 Anthropic의 2025~2026 engineering 사례가 개념을 구체화했으며, 더 넓게는 agent runtime, scaffolding, evaluation harness, platform engineering의 연속선에 있다.

### 8.2 하네스의 12개 구성요소

1. `mission contract`: 목표, scope, acceptance, stop/escalation
2. `instruction hierarchy`: system, organization, repository, task rule
3. `context builder`: relevant code, docs, errors, state, provenance
4. `state/memory`: durable progress, checkpoint, compaction, handoff
5. `typed tools`: schema, side-effect class, timeout, cancellation, errors
6. `environment`: worktree, container, terminal, browser, network
7. `identity/permission`: scoped credential, allow/ask/deny, approval
8. `orchestration`: planning, routing, subagent, concurrency, retry
9. `verification`: lint, typecheck, test, build, security, runtime QA
10. `observability`: prompt/tool/model/version/trace/cost/outcome
11. `human control`: preview, diff, approval, override, kill switch
12. `feedback loop`: recurring error를 rule, skill, lint, test, eval로 승격

### 8.3 reference architecture

```text
Task/Issue
→ risk + acceptance classifier
→ workspace provisioner
→ context builder
→ planner / task DAG
→ observe-decide-authorize-execute loop
→ deterministic gates
→ inferential review gates
→ human handoff: diff + evidence + risk + cost + trace
→ normal CI/CD
→ production feedback
→ rule/skill/lint/eval update
```

### 8.4 주요 contract

#### Tool contract

- typed input/output
- side-effect: read/write/execute/network/admin
- idempotency와 retry 안전성
- timeout/cancel
- stable error taxonomy
- credential scope
- tool result는 untrusted data
- secret 없는 audit event

#### Context contract

- repository-local, versioned source of truth
- 짧은 entry point와 progressive disclosure
- source, owner, date, validity
- compaction 후에도 intent와 acceptance 보존
- chat 밖 durable state

#### Multi-agent contract

- owner와 writable scope
- worktree/branch isolation
- dependency DAG
- bounded concurrency
- parent의 integration 책임

#### Completion contract

- agent가 “완료”라고 말한 것은 증거가 아님
- evidence가 acceptance item과 1:1로 연결
- test를 통과해도 runtime, security, maintainability를 별도 판단

### 8.5 OpenAI 사례를 과장하지 않는 법

OpenAI의 harness engineering 사례는 repository knowledge, worktree별 실행환경, UI·log·metric 가시성, 구조적 lint, agent review, 지속적인 “garbage collection”의 가치를 잘 보여준다. 그러나 특정 greenfield 내부 제품의 “10배 빠름”을 일반 생산성 법칙으로 옮기면 안 된다. 같은 수준의 repository legibility, CI, observability, sandbox, feedback loop 투자가 있어야 한다.

## 9. 코드 어시스턴트와 coding agent

### 9.1 분류

- `inline completion`: 현재 cursor 주변 코드 제안
- `chat assistant`: 설명·질문·snippet
- `edit agent`: 여러 파일 변경과 diff
- `terminal agent`: shell, git, tests를 포함한 repository 작업
- `IDE agent`: editor state, LSP, diff, terminal 통합
- `cloud/background agent`: 격리된 원격 runtime에서 비동기 작업과 PR
- `app builder`: 요구에서 앱·배포 artifact까지 생성
- `agent platform`: runtime, sandbox, browser, orchestration을 제공

### 9.2 대표 제품 지도

| 제품 | 핵심 surface | 강점이 되는 상황 | 강사가 확인할 위험 |
|---|---|---|---|
| OpenAI Codex | CLI, IDE, desktop, cloud | repository 작업과 장기 agent loop | local/cloud/GitHub 경계, feature별 GA/preview |
| Claude Code | terminal, IDE, desktop/cloud | 긴 coding task, hooks, subagents | provider route, managed settings, agent teams experimental |
| GitHub Copilot | IDE, CLI, coding agent, app | GitHub PR 중심 조직 | local agent와 enterprise control 경계, personal key, MCP |
| Gemini CLI/Code Assist | open CLI, IDE | Google ecosystem, terminal agent | stable/preview channel, local-admin policy 우회, MCP preview |
| Cursor | agent IDE, background VM | IDE-first agent workflow | background internet/auto-run/data retention, policy conflict |
| Windsurf | Cascade IDE | IDE-integrated team workflow | plan/contract별 retention과 enterprise control |
| Cline | IDE/CLI, plan/act | BYOK와 명시적 승인 workflow | YOLO auto-approval, inference provider 전송 |
| Roo Code | IDE modes/orchestrator | mode별 역할과 checkpoint | 중앙 enforcement 공개 증거 부족, setting export key |
| Aider | terminal pair programmer | 명시적 file context, git, lint/test | broad orchestration보다 focused workflow |
| OpenHands | runtime/container/browser platform | self-hosted agent experimentation | local GUI는 multi-tenant용 아님, Enterprise와 구분 |
| SWE-agent | research harness | trajectory와 eval 교육 | enterprise governance 제품이 아님 |
| JetBrains Junie | JetBrains IDE agent | IntelliJ-native workflow | 지원 IDE·언어·조직 정책 |
| AWS Q Developer | IDE/CLI/AWS | AWS workload와 계정 context | IAM, telemetry, region, data boundary |
| Devin | hosted autonomous agent | issue-to-PR 장기 작업 | cloud data, network, cost, review |
| Replit Agent/Lovable/Bolt/v0 | app builder | greenfield prototype | generated dependency, security, maintainability, lock-in |
| TECHAI Code | 사내 CLI/VS Code | 내부 model, knowledge, MCP, policy | exact build, model, tools, permission, logs, governance |

제품의 “GA”는 모든 feature가 안정이라는 뜻이 아니다. 예를 들어 Copilot의 coding agent, CLI, app은 각각 다른 시점에 GA가 됐고 sandbox는 preview일 수 있다. Claude Code 자체는 GA지만 agent teams는 experimental이다. 제품보다 surface와 feature의 lifecycle을 확인한다.

### 9.3 제품 비교 rubric

1. 실행 위치: local, cloud, hybrid
2. 읽는 data: open file, repo, organization, external systems
3. 쓰는 범위: suggestion, workspace, branch, PR, deploy
4. tool: shell, browser, git, LSP, MCP
5. model 선택과 routing
6. context/rules/skills/memory
7. approval와 policy enforcement
8. sandbox, network, secret isolation
9. subagent와 concurrency
10. session durability와 compaction
11. test/build/runtime QA
12. audit log와 OpenTelemetry
13. retention, training use, residency, deletion
14. enterprise SSO/RBAC/budget
15. 비용, latency, human review time

### 9.4 agentic coding production loop

```text
Issue/spec
→ acceptance와 위험 분류
→ frozen sample 또는 isolated worktree
→ read-only repository mapping
→ 작은 plan
→ smallest correct change
→ format/typecheck/test/build/security
→ 실제 surface QA
→ diff와 evidence review
→ PR와 normal CI
→ deploy/observe
→ 반복 실패를 rule/skill/test/eval로 환류
```

### 9.5 anti-pattern

- vague prompt 한 줄로 큰 rewrite
- 전체 repository를 context에 무조건 넣음
- test를 지우거나 약화해 green
- 존재하지 않는 dependency 설치
- agent가 만든 코드가 많다는 것을 생산성으로 측정
- 동일 branch를 여러 agent가 동시 수정
- background agent에 ambient credential 제공
- diff를 안 보고 “잘 됐어?”라고 다시 물음
- review agent가 같은 모델이라 독립 검증이라고 믿음
- agent 종료를 완료로 처리

## 10. 평가와 benchmark

### 10.1 2026 coding benchmark의 핵심 사건

- OpenAI는 2026-02 SWE-bench Verified 사용 중단을 발표했다.
- OpenAI는 2026-07-08 SWE-bench Pro도 약 30%가 broken일 수 있다고 보고 후속 추천을 철회했다.
- 문제 유형: 지나치게 엄격한 test, 불충분한 prompt, 낮은 test coverage, misleading prompt.
- 2026-07-29 현재 널리 합의된 단일 successor는 없다.
- 최신 Stanford AI Index가 Verified의 “거의 100%”를 capability headline으로 사용하지만, 이후 benchmark audit과 함께 읽어야 한다. 공식 보고서도 benchmark validity 변화보다 늦을 수 있다는 좋은 교육 사례다.

### 10.2 사용할 수 있는 portfolio

| 평가 | 볼 수 있는 것 | 한계 |
|---|---|---|
| SWE-rebench | 지속 갱신 repository task | 공개 후 contamination, task audit 필요 |
| SWE-bench-Live | 최신 multi-language/OS task, trajectory | 자동 curation만으로 validity 보장 안 됨 |
| Terminal-Bench 2.x | terminal execution과 환경 작업 | repository maintenance 전용이 아님 |
| FeatureBench | end-to-end feature | 자동 생성 task/test audit 필요 |
| RoadmapBench | 장기 version upgrade | 공개 gold/history 모방 가능 |
| CodeClash | 지속적 multi-round coding | 실제 PR maintenance와 다름 |
| GDPval | 전문직 author·verification | coding-agent 직접 대체 아님 |
| LiveBench | 주기 갱신 객관식·코딩 broad suite | snapshot date 필수 |
| Artificial Analysis | cost/time을 포함한 cross-vendor recipe | private task와 model judge 포함 |

### 10.3 사내 eval 설계

1. 공개 benchmark는 참고용으로만 사용
2. 의사결정 task는 fresh, private, time-split
3. 현업 engineer가 task를 작성하거나 완전 audit
4. model, harness, prompt, tool, network, compute, budget 고정
5. multiple seeds
6. hidden test와 solution은 workspace 밖
7. regression, property, mutation, differential test
8. no-change·abstention·policy task 포함
9. trajectory와 unnecessary action 검사
10. security violation, scope expansion, secret access 측정
11. cost, wall time, human review minutes 측정
12. maintainability, revert, post-merge incident 측정

### 10.4 평가의 5개 층

- `model capability`: 제한된 입력에서 model 자체의 성능
- `agent task outcome`: 환경에서 최종 상태가 목표를 충족
- `trajectory`: 어떤 도구와 경로로 도달했는지
- `safety/policy`: 금지 행동, 권한, data boundary 준수
- `organizational outcome`: lead time, quality, review load, incident, 사용자 가치

### 10.5 observability 최소 필드

- model, version, reasoning effort
- system/task prompt와 rule/skill/tool version
- source/provenance/trust label
- parent-child agent와 handoff
- tool name, sanitized args/result, latency, retry, approval
- retrieval doc ID, ranking, permission filter
- token, cache, cost, wall time
- state, stop reason, budget
- guardrail, human override
- outcome와 grader version

## 11. 보안

### 11.1 prompt injection은 해결된 문제가 아니다

웹페이지, README, 문서, issue, tool metadata, memory, 다른 agent의 메시지는 모두 instruction처럼 보일 수 있는 untrusted data다. “system prompt를 강하게 쓰면 해결”되지 않는다.

### 11.2 OWASP Agentic Top 10

1. ASI01 Agent Goal Hijack
2. ASI02 Tool Misuse
3. ASI03 Identity & Privilege Abuse
4. ASI04 Agentic Supply Chain Vulnerabilities
5. ASI05 Unexpected Code Execution
6. ASI06 Memory & Context Poisoning
7. ASI07 Insecure Inter-Agent Communication
8. ASI08 Cascading Failures
9. ASI09 Human-Agent Trust Exploitation
10. ASI10 Rogue Agents

### 11.3 최소 통제

- input/source trust label
- filesystem, process, network sandbox
- ambient secret 금지와 scoped identity
- tool allowlist와 side-effect 분류
- write/delete/send/admin 최종 경계 승인
- idempotent·reversible mutation
- time/token/turn/spend/recursion/concurrency limit
- signed/pinned plugin, skill, MCP manifest
- tool result schema validation과 sanitization
- delegation 시 re-authorization
- kill switch와 revocation
- 승인·override·실행 trace
- dependency registry, license, owner, vulnerability 확인
- memory source/version/expiry/delete

### 11.4 MCP security checklist

```text
Owner는 누구인가?
정확한 server와 version은?
stdio인가 remote인가?
어떤 data와 tool을 노출하는가?
read/write/admin을 구분했는가?
credential의 audience와 scope는?
tool description을 누가 검토했는가?
prompt injection data가 들어오는가?
로그에 prompt, file, token, PII가 남는가?
timeout, revoke, rollback은?
사용자에게 source와 side effect를 보여주는가?
```

MCP tool annotation이나 `readOnlyHint`는 보안 강제가 아니라 힌트다. 신뢰한 server, 실제 authorization, 실행환경 통제가 필요하다.

## 12. 개인정보·법·거버넌스

### 12.1 대한민국

대한민국 인공지능기본법은 2026-07-21 시행됐다. 고영향 AI 관련 사업자에게 위험관리, 기술적으로 가능한 설명, 이용자 보호, 사람의 관리·감독, 조치 문서의 작성·보관을 요구한다. 강의에서 법률 자문처럼 단정하지 말고 사내 법무·준법과 실제 적용성을 확인한다.

개인정보보호위원회의 2025 생성형 AI 안내서는 lifecycle 전체에서 목적·법적 근거·최소수집, privacy by design, data provenance, 가명처리, model/system 통제, 배포 전 test, 이용자 권리, 투명성, governance를 다룬다.

금융 업무에서는 “AI가 최종 판단”이 아니라 임직원의 관리·감독, 보조수단성, 보안, 신뢰성, 책임을 강조한다.

### 12.2 수업 data rule

- 실제 고객정보, 개인정보, 운영계 data 금지
- password, API key, token, 인증서, private key 금지
- 승인되지 않은 운영 code와 내부 문서 금지
- screenshot, log, 질문 공유 전에 masking
- sample repository와 synthetic secret만 사용
- 사고 시 즉시 중단, helper 보고, credential revoke, log 보존/삭제 절차

### 12.3 조직 도입

DORA 2025의 핵심은 AI가 조직의 강점과 약점을 증폭한다는 것이다. 도구 구매보다 다음 조직 능력이 ROI를 좌우한다.

1. 명확하고 공유된 AI stance
2. 건강한 data ecosystem
3. AI가 접근 가능한 내부 data
4. 강한 version control
5. small batches
6. user-centric focus
7. quality internal platforms

NIST AI RMF의 `Govern, Map, Measure, Manage`도 agent 도입의 운영 framing으로 사용할 수 있다.

## 13. 생산성과 경제성

### 13.1 안전한 결론

> AI coding 생산성은 과업 구조, 개발자 경험, repository context, model과 harness, 검토 방식, 측정지표에 따라 달라진다. 생성 code와 PR 수 증가는 사용자 가치, 품질, 이해도, lead time 개선과 동일하지 않다.

METR의 연구는 이 분야의 불확실성을 잘 보여준다.

- early-2025 숙련 open-source developer 연구: 당시 도구 사용 시 약 19% 느림
- late-2025/early-2026 update: speedup 가능성은 보이지만 selection과 시간 측정 문제로 확정 추정 불가
- early-2026 self-report: 1.4~2배 가치 증가를 보고했지만 self-report 규모를 그대로 믿기 어렵다고 명시

### 13.2 total task cost

```text
model token
+ prompt cache
+ sandbox/compute
+ tool/API/network
+ retry/failed run
+ CI
+ specification
+ supervision
+ review
+ integration/rework
+ expected incident
```

### 13.3 사내 효과 측정

- task completion과 acceptance
- lead time과 cycle time
- review minutes
- escaped defect와 revert
- change failure rate와 recovery
- security/policy incident
- developer cognitive load와 학습
- 사용자 value
- total cost per accepted change

## 14. SBTI 3일 재설계

현재 운영 문서는 `120분 × 3회 × 회차당 40명`을 전제로 한다. 실제로 같은 120명이 매일 참석하는 3일 종일 과정이면 아래 시간을 비례 확장하고 운영 인력을 늘려야 한다.

### Day 1: 모델·에이전트 지형과 안전한 단일 agent loop

학습 결과:

- 모델, 제품, agent, harness, tool을 구분
- workflow와 agent의 선택 기준 설명
- 작은 변경을 위임하고 diff·test로 검증
- 위험한 tool request를 거절

| 시간 | 내용 |
|---:|---|
| 0–10 | 목표, 환경 확인, 5분 안전 briefing |
| 10–30 | LLM·model family·reasoning·multimodal |
| 30–50 | agent loop, workflow 대 agent, system 계층 |
| 50–65 | Web/IDE/CLI/cloud coding agent 비교 demo |
| 65–90 | Lab 1: read-only repository mapping |
| 90–108 | Lab 2: 작은 change, diff, test |
| 108–116 | 악성 README·과도한 permission 거절 drill |
| 116–120 | exit ticket |

결과물:

- repository map
- 받아들인 변경 1개와 evidence
- 거절한 행동 1개와 이유

### Day 2: Context, RAG, MCP, harness, multi-agent

학습 결과:

- long context, RAG, memory, skill 차이 설명
- MCP의 역할과 신뢰 경계 설명
- harness 12개 요소로 coding agent 분석
- single과 multi-agent를 비용·품질로 비교

| 시간 | 내용 |
|---:|---|
| 0–12 | Day 1 retrieval quiz |
| 12–30 | context engineering, RAG, memory |
| 30–48 | MCP/A2A/AG-UI/ACP protocol map |
| 48–68 | harness engineering reference architecture |
| 68–92 | Lab 3: cited knowledge retrieval과 stale source 탐지 |
| 92–108 | Lab 4: single 대 multi-agent 비교 |
| 108–116 | eval card 작성 |
| 116–120 | exit ticket |

결과물:

- citation이 있는 knowledge answer
- MCP trust checklist
- single/multi-agent 비교표

### Day 3: 사내 framework 적용, 평가, 운영

학습 결과:

- TECHAI class build의 model/tool/permission/MCP 경계 확인
- framework knowledge를 근거로 제한된 변경 수행
- deterministic·inferential·human gate 구성
- privacy, log, rollback, incident를 설명

| 시간 | 내용 |
|---:|---|
| 0–15 | class release manifest와 build boundary |
| 15–32 | ProFrame/WebSquare/Wiki knowledge의 ownership·freshness |
| 32–75 | Capstone: bounded framework change |
| 75–92 | test/build/runtime QA와 evidence pack |
| 92–104 | peer review와 policy review |
| 104–114 | prompt injection, secret, rollback incident drill |
| 114–120 | assessment와 transfer plan |

결과물:

- bounded diff
- test/build/runtime evidence
- source/version citation
- 위험과 rollback note

## 15. 120명 운영

### 15.1 40명씩 3회인 경우

- 4명 × 10개 조
- lead instructor 1
- technical lead 또는 공동 진행 1
- helper 2
- host 1
- 최소 5명 운영 목표

### 15.2 같은 120명이 동시에 참석하는 경우

- 4명 × 30개 조
- lead instructor 1
- technical lead 1
- 5개 조당 helper 1, 총 6
- host/시설·출석 1
- 최소 9명 운영 목표

이는 법칙이 아니라 사내 계정·network·AI 실습 조건에 맞춘 시작점이다. T-7 실제 장소 rehearsal의 요청 대기시간과 성공률로 조정한다.

### 15.3 조별 역할

- Driver: keyboard
- Navigator: requirement와 다음 단계
- Reviewer: diff, test, 위험
- Recorder: error와 해결 기록

15~20분마다 교대한다.

### 15.4 preflight

- OS, VS Code, Git, terminal version
- SSO, 개인 API key, model entitlement
- exact VSIX/CLI artifact와 SHA-256
- network, VPN, proxy, firewall
- API concurrency와 quota
- sample repo와 frozen dependency
- offline ZIP, captured output, local HTML/video
- synthetic secret와 prompt injection drill
- incident contact와 kill switch

관련 운영자료:

- [강의 운영 준비 가이드](/Users/jiwonkim/kimjiwon_slide/docs/SBTI_강의_운영준비_2026-07-29.md)
- [40석 리허설 체크리스트](/Users/jiwonkim/kimjiwon_slide/docs/SBTI_40석_리허설_체크리스트.md)
- [참가자 사전안내](/Users/jiwonkim/kimjiwon_slide/docs/SBTI_참가자_사전안내_초안.md)
- [수치·주장 근거팩](/Users/jiwonkim/kimjiwon_slide/docs/SBTI_수치·주장_근거팩_템플릿.md)
- [강사 학습노트와 Q&A](/Users/jiwonkim/kimjiwon_slide/docs/SBTI_강사_학습노트_2026-07-29.md)

## 16. 강의용 release manifest

```text
Class/date/owner:
Artifact source and immutable path:
Component: VSIX / CLI / standalone IDE:
Artifact filename, platform, variant:
SHA-256:
Extension manifest version:
Embedded server build/version:
Config directory and config path:
Effective model defaults: Fast / Super / Dev / Parse:
Tool inventory: /tools/catalog output and timestamp:
MCP inventory: server / version / transport / endpoint / auth / tools / status:
Permission policy: exact path / schema / allow-ask-deny / autopilot:
Network/SSO prerequisites:
Prompt/response/tool/error log scope:
Retention/readers/deletion:
Known limitations:
Offline fallback:
Live smoke result and timestamp:
Approval to distribute:
```

현재 후보 bundle에서는 다음이 확인됐다.

- VSIX manifest: `0.1.107`
- 내장 server `--version`: `tgc-server dev`
- source 기본 config: vanilla `~/.tgc`, on-prem build intent `~/.tgc-onprem`
- source permission path: active config dir의 `permissions.yaml`
- source MCP REST handling: `stdio`, `sse`
- tool catalog는 built-in, VS Code client, MCP tool을 동적으로 합치므로 source list만으로 정확한 숫자를 말할 수 없음

## 17. 강사 14일 학습계획

### P0: 수업 전에 막힘없이 설명·시연

| 날짜 | 공부·실행 | 완료 증거 |
|---:|---|---|
| 1 | model/LLM/token/Transformer/training/inference | 10분 whiteboard 설명 |
| 2 | reasoning, multimodal, open-weight, cost/latency | model 비교표 |
| 3 | workflow와 agent loop, tool calling | 단일 agent trace |
| 4 | context engineering, long context, compaction | bad/good context 비교 |
| 5 | RAG, retrieval eval, memory | citation RAG 실습 |
| 6 | MCP host/client/server와 security | read-only MCP와 trust card |
| 7 | A2A, AG-UI, ACP, Skills, LSP | protocol layer diagram |
| 8 | harness 12요소와 reference architecture | TECHAI harness 분석 |
| 9 | code assistant 10종을 rubric으로 비교 | vendor-neutral matrix |
| 10 | single/multi-agent 비교 | cost/quality 실험표 |
| 11 | eval, benchmark failure, observability | private eval 5개 |
| 12 | OWASP, injection, secrets, sandbox | incident drill |
| 13 | 한국 법, 개인정보, 사내 log·MCP·수치 | 승인·근거 pack |
| 14 | 40석 rehearsal과 teach-back | GO/NO-GO record |

### P1: 강의 품질을 높이는 주제

- inference serving와 KV/prompt cache
- quantization, LoRA, distillation
- hybrid retrieval와 reranking
- agent identity와 delegated authorization
- OpenTelemetry GenAI semantic conventions
- property/mutation testing
- causal productivity measurement
- platform engineering와 internal developer platform

### P2: 질문이 나올 때 정확히 범위를 말할 수 있으면 되는 주제

- recursive self-improvement
- self-improving memory
- agent marketplace와 registry federation
- generative UI/A2UI
- formal verification agent
- embodied/robotic agent
- decentralized swarm

## 18. 강사가 받아야 할 어려운 질문

### 모델

**Q. reasoning model은 일반 LLM과 다른가?**  
A. 같은 foundation family에 reasoning post-training과 더 큰 test-time compute를 적용하는 경우가 많다. 제품명이 아니라 effort, latency, token, tool loop를 함께 봐야 한다.

**Q. chain of thought를 보여주면 믿을 수 있나?**  
A. reasoning summary는 유용한 설명일 수 있지만 실제 내부 원인의 충실한 기록이라고 보장할 수 없다. 결과와 외부 증거를 검증한다.

**Q. context가 1M이면 RAG가 필요 없나?**  
A. 아니다. 필요한 source 선택, freshness, ACL, citation, retrieval cost 문제는 남는다.

**Q. open source 모델이 사내에 더 안전한가?**  
A. data egress를 줄일 수 있지만 운영 취약점, supply chain, patch, access control, logging 책임이 사내로 이동한다. 라이선스도 별도다.

### Agent

**Q. agent와 workflow의 차이는?**  
A. 다음 행동과 분기를 모델이 동적으로 고르는 정도다. 안정된 경로는 workflow가 더 싸고 예측 가능하다.

**Q. agent가 알아서 끝까지 하면 왜 사람이 필요한가?**  
A. 목표·가치·권한·예외·책임은 자동으로 결정되지 않는다. 사람은 specification, risk, acceptance, override를 소유한다.

**Q. 여러 agent면 더 정확한가?**  
A. 독립 증거와 역할 분리가 있을 때 가능하다. 같은 모델·prompt를 복제하면 상관 오류와 비용만 늘 수 있다.

**Q. subagent와 A2A agent는 같은가?**  
A. subagent는 한 runtime 내부 delegation일 수 있다. A2A는 독립·opaque agent application 사이의 protocol이다.

### Context와 지식

**Q. 문서를 지식화하면 모델이 학습되나?**  
A. 보통 weight training이 아니라 parsing, indexing, retrieval, context injection이다.

**Q. memory를 많이 저장할수록 좋은가?**  
A. stale, poisoned, private memory가 누적될 수 있다. 선택, source, expiry, deletion이 필요하다.

**Q. citation이 있으면 정확한가?**  
A. citation이 실제 주장을 support하는지, source가 최신·권위 있는지 확인해야 한다.

### MCP와 protocol

**Q. MCP는 REST API를 대체하나?**  
A. 아니다. agent가 tool/data capability를 발견·호출하는 공통 interface이며 실제 backend가 REST일 수 있다.

**Q. MCP server를 붙이면 안전한가?**  
A. 아니다. 설치와 연결은 trust가 아니다. owner, code, scope, credential, data, log, rollback을 검토한다.

**Q. A2A와 MCP 중 무엇을 선택하나?**  
A. tool/data capability면 MCP, 독립 agent와 task/artifact를 주고받으면 A2A다. 함께 쓸 수 있다.

**Q. ACP가 MCP를 대체하나?**  
A. ACP는 editor와 coding agent, MCP는 agent와 tool/data server 사이를 표준화한다.

### Coding과 평가

**Q. 어떤 code assistant가 최고인가?**  
A. task, repository, language, data boundary, execution surface, policy, budget에 따라 다르다. 같은 private eval로 비교한다.

**Q. SWE-bench 점수로 고르면 안 되나?**  
A. task defect, contamination, harness 차이가 크고 Verified와 Pro 모두 신뢰 문제가 확인됐다. portfolio와 private eval이 필요하다.

**Q. test를 통과했으면 끝인가?**  
A. test coverage 밖의 오류, security, maintainability, UI behavior가 남는다. runtime QA와 review가 필요하다.

**Q. AI code가 많아지면 생산성이 오른 것 아닌가?**  
A. output volume은 가치가 아니다. accepted change, review time, defect, lead time, incident, 사용자 결과를 측정한다.

### 보안과 조직

**Q. system prompt로 injection을 막을 수 있나?**  
A. 단독으로는 안 된다. untrusted data 분리, least privilege, sandbox, approval, egress control이 필요하다.

**Q. allow/ask/deny면 충분한가?**  
A. ask는 안전 판단이 아니라 승인 요청이다. 승인 피로, tool 조합, autopilot, background execution을 고려해야 한다.

**Q. ZDR이면 data가 아무 데도 안 남나?**  
A. 적용 product, model provider, client, trace, MCP, local log, 예외 feature를 확인해야 한다. 하나의 ZDR 문구를 전체 system에 전이하면 안 된다.

**Q. AI가 만든 결과의 책임은 누구에게 있나?**  
A. 배포·업무 판단을 승인한 조직과 사람이 책임 구조를 가져야 한다. agent에게 책임을 넘길 수 없다.

## 19. 전체 키워드 지도

아래는 제품 암기 목록이 아니라 질문을 분류하는 map이다.

### 19.1 AI·모델 기초

- AI: 지능적 업무를 수행하는 system의 넓은 범주
- ML: data에서 pattern을 학습
- Deep learning: 다층 neural network 기반 ML
- Foundation model: 다양한 task에 적응하는 사전학습 모델
- LLM/SLM: 대규모/소규모 language model
- Multimodal: text·image·audio·video 등 복수 modality
- Token/tokenizer: model의 입력 단위와 분해기
- Embedding/vector: 의미를 수치 공간에 표현
- Parameter/weight: 학습으로 정해진 model 값
- Transformer: attention 기반 sequence architecture
- Attention/self-attention: token 사이 관련성 계산
- Positional encoding: sequence 위치 정보
- Next-token prediction: 다음 token 확률을 학습·생성
- Pretraining: 대규모 일반 학습
- Scaling law: data·compute·parameter와 성능의 경험 관계
- Emergent capability: scale에서 새롭게 관찰되는 행동
- Jagged frontier: task별 능력이 고르지 않은 현상
- Hallucination: 근거 없는 내용 생성
- Calibration: confidence와 실제 정확도의 일치
- Uncertainty/abstention: 불확실성 표현과 답변 보류

### 19.2 학습·정렬·경량화

- SFT/instruction tuning: 지시-응답 예제로 행동 조정
- RLHF/RLAIF: 사람/AI feedback 기반 강화학습
- Preference optimization: 선호 pair로 응답 성향 학습
- DPO/PPO/GRPO: 대표 preference/RL optimization 방식
- Distillation: 큰 model 행동을 작은 model로 전달
- Fine-tuning: domain/task data로 weight 조정
- LoRA/PEFT: 일부 parameter로 효율적 fine-tuning
- Quantization: 낮은 bit 정밀도로 serving 효율화
- Pruning: 덜 중요한 weight·구조 제거
- MoE/expert routing: 일부 expert만 활성화
- Synthetic data: model 등이 생성한 학습 data
- Data contamination: 평가 data가 학습에 섞임
- Benchmark leakage: test 정보가 model/harness에 노출
- Continual learning: 배포 후 지속 학습
- Model collapse: 재생성 data 반복 학습의 품질 저하
- Alignment: 사람·조직 의도와 행동을 맞추는 과정
- Safety tuning: 위험 요청 대응 조정
- Reward hacking: 점수 기준의 허점을 이용
- Eval gaming: 실제 능력 대신 평가를 공략

### 19.3 추론·serving

- Inference: 요청에 model을 실행
- Reasoning effort: 요청당 추론 budget
- Test-time compute: inference 시 추가 계산
- Context window: 입력·출력 token 범위
- Effective context: 실제로 유용하게 활용되는 범위
- KV cache: attention 중간값 cache
- Prompt cache: 반복 prefix 계산 cache
- TTFT/TPS: 첫 token 시간/초당 token
- Latency/throughput: 지연/처리량
- Batch: 여러 요청 묶음 처리
- Streaming: token/event 점진 전송
- Speculative decoding: 작은 model 예측으로 생성 가속
- Constrained decoding: schema 등 허용 출력 제한
- Structured output/JSON Schema: 형식 제약 출력
- Function calling/tool calling: 구조화된 도구 요청
- Temperature/top-p: sampling 다양성 조절
- Seed/determinism: 재현성 관련 설정
- Rate limit/quota: 요청·token 한도
- Routing/fallback: model 선택과 대체
- Cost per accepted task: 승인된 결과당 총비용

### 19.4 Context·RAG·memory

- Prompt engineering: 지시 작성
- Context engineering: 필요한 정보·상태 구성
- Context rot: context가 커지며 품질 저하
- Lost in the middle: 중간 정보 활용 저하
- RAG: 검색 증강 생성
- Dense/sparse retrieval: embedding/keyword 검색
- Hybrid retrieval: dense+sparse 결합
- Chunking: 문서 분할
- Metadata filtering: 속성 기반 검색 제한
- ACL-aware retrieval: 권한을 반영한 검색
- Query rewriting: 검색 질의 개선
- Reranking: 후보 재정렬
- Grounding: 외부 근거에 답을 연결
- Provenance: source와 계보
- Citation correctness: 인용이 주장을 실제 지원
- Knowledge graph/GraphRAG: entity·relation 기반 검색
- Vector DB: embedding index 저장
- Recall@k/precision@k: 검색 recall/precision
- MRR/nDCG: ranking 품질
- Working/episodic/semantic/procedural memory: memory 유형
- Compaction: 오래된 실행 상태 압축
- Checkpoint: 복구 가능한 상태 저장
- Memory poisoning: 악성·오류 memory 주입
- Freshness/expiry/deletion: 최신성·만료·삭제

### 19.5 Agent·멀티에이전트

- Agent/workflow/autonomy: 동적 결정과 자율성
- Observe-think-act loop: 관찰·판단·행동 반복
- ReAct: reasoning과 action의 반복 pattern
- Plan-and-execute: 계획과 실행 분리
- Prompt chaining: 단계 연결
- Router: task를 model/agent/tool로 분배
- Parallelization: 독립 작업 병렬화
- Evaluator-optimizer: 생성·평가 반복
- Reflection/critic: 자기·외부 비평
- Planner/executor/reviewer: 역할 분리
- Supervisor-worker: 관리자와 worker
- Agent-as-tool: agent를 tool처럼 호출
- Subagent: 한 runtime 내부 위임
- Handoff: 업무 소유권 인계
- Blackboard: 공용 상태 기반 협업
- Swarm: 다수 agent의 분산 협업
- DAG/state machine: dependency·상태 모델
- Human-in/on/out-of-the-loop: 사람 개입 수준
- Termination/stop condition: 종료 기준
- Retry/backoff: 재시도 정책
- Idempotency: 반복 실행의 안전성
- Rollback/compensation: 변경 복구
- Budget: token·time·cost·turn 한도
- Computer/browser use: UI·browser 행동
- Correlated error: 여러 agent의 공통 오류

### 19.6 Protocol·interoperability

- MCP host/client/server: tool/data protocol 역할
- MCP tool/resource/prompt: 제공 capability
- stdio/Streamable HTTP/SSE: 연결 transport
- JSON-RPC: message protocol
- Capability negotiation: 지원 기능 협상
- Tasks/extensions/apps: MCP 확장 영역
- OAuth/OIDC/mTLS/API key: 인증 방식
- A2A Agent Card: agent discovery metadata
- A2A message/task/artifact: 협업 객체
- A2A streaming/push: 비동기 상태 전달
- AG-UI event/state/interrupt: agent UI 상호작용
- A2UI/generative UI: 선언적 UI 생성
- ACP session/plan/diff/permission: editor-agent UX
- LSP diagnostics/definition/reference: code intelligence
- OpenAPI/gRPC/WebSocket: 기존 service interface
- Agent Skills/SKILL.md: 절차 package
- AGENTS.md/CLAUDE.md/GEMINI.md: repository instruction entry
- Rules/hooks/plugins: 행동 규칙·event extension
- Semantic versioning/conformance/TCK: 호환성과 시험

### 19.7 Harness·platform

- Harness engineering: agent runtime/control engineering
- Scaffolding: agent가 일할 구조와 지원물
- Environment provisioning: workspace 실행환경 생성
- Sandbox/container/VM: 격리 실행
- Worktree/branch: 변경 격리
- Scoped identity: 업무별 제한된 principal
- Secret broker: 제한된 자격증명 전달
- Allow/ask/deny: permission policy
- Least privilege: 최소 권한
- Policy as code: 실행 가능한 정책
- Typed tool/tool schema: 구조화 capability
- Side-effect classification: 읽기·쓰기·실행·전송 분류
- Durable state: context 밖 지속 상태
- Orchestration: agent와 tool 조정
- Concurrency control: 병렬 수 제한
- Timeout/cancellation: 실행 중단
- Trace/telemetry: 실행 관측
- Deterministic gate: test·build 등 기계 판정
- Inferential gate: rubric·review 기반 판정
- Human approval/override: 사람 통제
- Kill switch: 긴급 중단
- Garbage collection/entropy control: 지속적 품질 정리
- Internal developer platform: 공통 개발 self-service 기반

### 19.8 Coding agent·SDLC

- Inline completion/chat/edit/agent mode
- Local/cloud/background agent
- Repo map: repository 구조 요약
- Text search/AST/LSP: code 탐색 수단
- Patch/diff: 변경 표현
- Format/lint/typecheck/test/build
- Unit/integration/E2E/property/mutation test
- CI/CD, PR, code review
- SAST/DAST/SCA/SBOM
- Dependency hallucination/slopsquatting
- Supply-chain security
- Spec-driven development
- TDD/BDD
- Trunk-based development
- Worktree/checkpoint/revert/reflog/bisect
- Vibe coding: 빠른 자연어 중심 생성
- Agentic coding: agent가 탐색·수정·검증
- Long-running agent: context window를 넘어 지속 작업
- Repository legibility: agent가 구조·규칙·상태를 읽을 수 있음
- Architecture test: dependency·layer invariant 검증
- AI slop: 중복·불필요 추상화·근거 없는 코드

### 19.9 Eval·observability

- Offline/online eval
- Golden set/fresh/private/time-split eval
- Pass@k/pass@1
- Task success/outcome grader
- Trajectory grader
- LLM-as-judge
- Pairwise/rubric/blind review
- Inter-rater agreement
- Multiple seeds/confidence interval
- Flakiness/infrastructure noise
- Contamination/saturation/broken task
- Cost-adjusted success
- Wall time/human review minutes
- Abstention/no-change task
- Scope expansion/policy violation
- Regression/revert/escaped defect
- Lead time/change failure/time to restore
- Trace/span/log/metric
- OpenTelemetry GenAI conventions
- Prompt/tool/model versioning
- Evaluation harness

### 19.10 Security·governance

- Prompt injection/indirect injection
- Jailbreak
- Data exfiltration
- Tool poisoning
- MCP rug pull
- Confused deputy
- Excessive agency
- Identity/privilege abuse
- Memory poisoning
- Insecure inter-agent communication
- Cascading failure
- Unexpected code execution
- Human trust exploitation
- Rogue agent
- Egress control
- Tenant isolation
- Data residency/retention/deletion
- ZDR
- SSO/SCIM/RBAC/ABAC
- Audit log
- DPA/subprocessor/SOC 2
- AI risk assessment/model card/system card
- NIST AI RMF
- OWASP LLM/Agentic Top 10
- EU AI Act
- 대한민국 인공지능기본법
- 개인정보 lifecycle
- Human oversight/accountability

## 20. 강의 전날 변동 정보 refresh

- 현재 모델명, effort tier, 제공 plan
- code assistant의 GA/preview/experimental feature
- 정확한 class artifact와 checksum
- embedded server build
- model default와 quota
- tool catalog
- MCP server/version/transport/status
- permission path와 autopilot
- SSO, API key, VPN, proxy
- prompt/response/tool/log scope와 retention
- 모든 외부 링크
- 내부 운영 수치의 dated query
- POC 수치의 method와 승인
- protocol current revision
- benchmark version과 audit 상태

## 21. 핵심 출처

### 모델·산업

- [OpenAI GPT-5.6](https://openai.com/index/gpt-5-6/)
- [Anthropic Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5)
- [Google Gemini 3.5](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/)
- [DeepSeek V4 technical report](https://arxiv.org/abs/2606.19348)
- [NIST/CAISI DeepSeek V4 Pro evaluation](https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro)
- [Stanford 2026 AI Index](https://hai.stanford.edu/ai-index/2026-ai-index-report)
- [OSI Open Source AI Definition](https://opensource.org/ai/open-source-ai-definition)

### Agent·context·harness

- [OpenAI practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
- [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)
- [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic Long-running Agent Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic Agent Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

### Protocol

- [MCP 2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [A2A specification](https://a2a-protocol.org/latest/specification/)
- [AG-UI introduction](https://docs.ag-ui.com/introduction)
- [ACP introduction](https://agentclientprotocol.com/get-started/introduction)
- [Agent Skills specification](https://agentskills.io/specification)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/specs/semconv/)

### 평가·생산성

- [OpenAI: Why we no longer evaluate SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)
- [OpenAI: Separating signal from noise in coding evaluations](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)
- [Anthropic: Infrastructure noise](https://www.anthropic.com/engineering/infrastructure-noise)
- [METR developer productivity update](https://metr.org/blog/2026-02-24-uplift-update/)
- [METR early-2026 usage survey](https://metr.org/blog/2026-05-11-ai-usage-survey/)
- [DORA 2025 AI-assisted software development](https://dora.dev/research/2025/dora-report/)

### 보안·법·거버넌스

- [OWASP Agentic Top 10](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [대한민국 인공지능기본법 제34조](https://law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1031810839)
- [개인정보보호위원회 생성형 AI 개인정보 처리 안내서](https://www.pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS217&mCode=G010030000&nttId=11439)

## 22. 최종 강사 원칙

1. 제품명이 아니라 layer와 boundary를 가르친다.
2. 최신 정보에는 날짜, version, source를 붙인다.
3. vendor claim과 independent evidence를 분리한다.
4. model 점수와 agent system 성능을 분리한다.
5. agent의 말보다 environment의 evidence를 믿는다.
6. permission request는 safety proof가 아니다.
7. protocol adoption은 security adoption이 아니다.
8. long context, RAG, memory는 대체재가 아니라 다른 도구다.
9. multi-agent는 측정 가능한 이점이 있을 때만 쓴다.
10. 생성량이 아니라 accepted outcome과 total cost를 측정한다.
11. 안전·법·privacy를 마지막 부록이 아니라 첫 실습부터 넣는다.
12. 학생이 AI 없이 diff와 위험을 설명할 수 있어야 수업이 성공이다.

