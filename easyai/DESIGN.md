# SBTI4 AI 코딩 용어사전 Design System

## 1. Atmosphere & Identity

기술 용어를 처음 접하는 독자가 종이 교재처럼 편안하게 읽되, 핵심 문장과 에이전트 장면에서는 어두운 터미널의 집중감을 느끼는 편집형 교육 자료다. 시그니처는 밝은 문서 면 위의 파란 신뢰 표시와, 중요한 개념을 묶는 짙은 터미널 패널이다. 새 요소는 기존 교재의 정보 밀도를 흐리지 않고 근거·출처·권리 경계를 더 명확하게 해야 한다.

## 2. Color

| Role | Token | Value | Usage |
| --- | --- | --- | --- |
| Page | `--bg` | `#fafafa` | 전체 배경 |
| Surface | `--surface` | `#ffffff` | 카드·본문 면 |
| Soft surface | `--soft` | `#f4f7fb` | 쉬운 설명·보조 블록 |
| Border | `--line` | `#e2e7ee` | 구획선·카드 경계 |
| Text | `--text` | `#1a1a1a` | 본문 |
| Heading | `--dark` | `#111827` | 제목·강조 |
| Muted | `--muted` | `#5f6672` | 출처·보조 문구 |
| Accent | `--blue` | `#0066cc` | 링크·핵심 정보·포커스 |
| Info | `--cyan` | `#0ea5e9` | 쉬운 설명·터미널 포인트 |
| Success | `--green` | `#16a34a` | 확인된 사실 |
| Warning | `--orange` | `#ea580c` | 주의 |
| Secondary | `--purple` | `#7c3aed` | 보조 분류 |
| Error | `--red` | `#dc2626` | 오해·위험 |
| Terminal | `--terminal` | `#232832` | 인용·표지·집중 패널 |

- 새 권리·출처 요소는 `--surface`, `--soft`, `--line`, `--dark`, `--muted`, `--blue`, `--terminal`만 재사용한다.
- 장식용 새 색을 만들지 않는다.

## 3. Typography

| Level | Size | Weight | Line height | Usage |
| --- | --- | --- | --- | --- |
| Display | `clamp(34px, 6vw, 58px)` | 800 | 1.18 | 표지 제목 |
| Chapter | `clamp(22px, 3.4vw, 30px)` | 800 | inherited | 장 제목 |
| Term title | `19px` | 800 | inherited | 용어 카드 제목 |
| Body | `16px` | 400 | 1.7 | 기본 본문 |
| Body compact | `15px–15.5px` | 400 | inherited | 카드 설명 |
| Metadata | `12.5px–13.5px` | 400–700 | inherited | 출처·권리·상태 |

- Primary: `-apple-system, BlinkMacSystemFont, "SF Pro Text", Pretendard, "Segoe UI", sans-serif`
- Mono: `"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace`
- 한국어는 의미 단위가 한 글자만 고립되지 않도록 충분한 열 너비와 `word-break: keep-all` 성격을 유지한다.

## 4. Spacing & Layout

- 기본 단위는 4px이다. 기존 8·12·16·18·20·24·36·60px 리듬을 유지한다.
- 본문 최대 폭은 880px이며 좌우 안쪽 여백은 24px이다.
- 640px 이하에서는 그림·표·권리 카드가 한 열로 읽히고 수평 본문 스크롤이 생기지 않아야 한다.
- 출처 목록 뒤에 권리 블록, 발행 정보, 작성자 순으로 배치해 독자가 `근거 → 권리 → 책임 주체` 순서로 읽게 한다.
- A4에서는 푸터 전체가 별도 페이지에서 시작하되 권리 카드 하나가 페이지 중간에 잘리지 않게 한다.

## 5. Components

### TermCard

- **Structure**: `.term > .term-head + content blocks`
- **States**: 정적 콘텐츠. 검색 결과에서는 행 단위 `hidden`만 사용한다.
- **Accessibility**: 제목 계층과 자연스러운 문서 순서 유지.
- **Motion**: 없음.
- **Layout**: vertical stack.

### EvidenceBlock

- **Structure**: `.easy`, `.myth`, `.quote`, `.src`.
- **Variants**: 쉬운 설명, 오해/사실, 발표 문장, 근거 출처.
- **Accessibility**: 색만으로 의미를 전달하지 않고 라벨 텍스트를 함께 둔다.
- **Motion**: 없음.

### SidebarNavigation

- **Structure**: 고정 사이드바, 검색, 장 이동, 편집·인쇄 동작.
- **States**: default, hover, focus, active, collapsed, mobile open.
- **Accessibility**: 버튼 이름, `aria-expanded`, 키보드 포커스, 백드롭 닫기 경로 유지.
- **Motion**: 폭과 본문 여백 200ms 전환. reduced-motion에서는 기능을 방해하지 않는다.

### RightsCredit

- **Structure**: `.rights-panel > .rights-head + .rights-grid > .rights-item` 뒤에 `.rights-legal`.
- **Variants**: 직접 제작, AI 제작 보조, 인용·재구성, 상표·비제휴.
- **States**: 링크의 default, hover, focus. 정적 카드에는 hover 이동을 넣지 않는다.
- **Accessibility**: 명확한 제목과 짧은 문장, 충분한 대비, 실제 링크에는 밑줄과 포커스 표시.
- **Motion**: 없음.
- **Layout**: 데스크톱 2열 grid, 640px 이하 1열 stack, 인쇄 시 2열 유지 가능한 폭에서만 사용.

## 6. Motion & Interaction

| Type | Duration | Easing | Usage |
| --- | --- | --- | --- |
| Micro | `150ms` | `ease-out` | 링크·버튼 hover/focus |
| Standard | `200ms` | `ease` | 사이드바 폭·본문 여백 |

- 권리·출처 영역에는 장식 애니메이션을 넣지 않는다.
- `prefers-reduced-motion`에서 정보 접근에 필요한 상태 변화는 즉시 반영한다.

## 7. Depth & Surface

전략은 mixed다. 본문 카드와 권리 카드는 얇은 경계와 밝은 tonal shift로 분리하고, 모달·고정 내비게이션처럼 실제로 떠 있는 요소에만 그림자를 쓴다. 권리 카드는 법률 배지처럼 과도하게 보이지 않도록 기존 출처 푸터보다 한 단계만 강조한다.

## 8. Accessibility Constraints & Accepted Debt

### Constraints

- WCAG 2.2 AA를 목표로 한다.
- 모든 상호작용 요소는 키보드로 도달 가능하고 `:focus-visible` 표시가 있어야 한다.
- 375px에서 권리 문구의 잘림·겹침·수평 overflow가 없어야 한다.
- 200% 확대와 A4 인쇄에서 한국어 문장·영문 제품명이 잘리지 않아야 한다.
- AI 제작 보조, 제3자 인용, 상표 비제휴를 시각적 색만이 아니라 텍스트로 구분한다.

### Accepted Debt

| Item | Location | Why accepted | Owner / Exit |
| --- | --- | --- | --- |
| 기존 CSS의 일부 raw 색상·간격 | `index.html` | 기존 단일 파일 디자인을 그대로 보존하는 범위이며 이번 권리 표시에 새 raw 토큰을 추가하지 않음 | 다음 전체 디자인 시스템 정리 때 통합 |

