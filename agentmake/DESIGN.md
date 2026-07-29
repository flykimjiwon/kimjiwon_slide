# Agent Essentials Lecture Design System

## 1. Atmosphere & Identity

40명이 동시에 보는 기술 강의용 화면이다. 기존 `sbti3/index.html`의 밝은 캔버스, 선명한 블루, 모노스페이스 라벨, 넉넉한 여백을 계승한다. 시그니처는 에이전트를 하나의 채팅창이 아니라 여러 층이 맞물린 실행 시스템으로 보여주는 `agent stack`과 `bounded loop`다.

## 2. Color

| Role | Token | Value | Usage |
|---|---|---:|---|
| Canvas | `--canvas` | `#f6f9fd` | 전체 배경 |
| Surface | `--surface` | `#ffffff` | 주요 패널 |
| Surface soft | `--surface-soft` | `#edf4ff` | 보조 패널 |
| Ink | `--ink` | `#10243e` | 제목과 본문 |
| Ink soft | `--ink-soft` | `#4d627a` | 설명 |
| Line | `--line` | `#d8e4f2` | 경계 |
| Blue | `--blue` | `#0b6bdb` | 핵심 개념과 포커스 |
| Blue deep | `--blue-deep` | `#084b9b` | 활성 상태 |
| Blue pale | `--blue-pale` | `#dcecff` | 강조 배경 |
| Green | `--green` | `#13795b` | 성공, 검증, 허용 |
| Green pale | `--green-pale` | `#dcf5ea` | 검증 배경 |
| Amber | `--amber` | `#a45b08` | 승인, 주의 |
| Amber pale | `--amber-pale` | `#fff0d2` | 승인 배경 |
| Red | `--red` | `#b42318` | 거절, 중단 |
| Red pale | `--red-pale` | `#fee4e2` | 거절 배경 |
| Navy | `--navy` | `#0a1b30` | 타이틀 배경 |
| Navy soft | `--navy-soft` | `#17365f` | 타이틀 표면 |

Blue is the single brand accent. Green, amber, and red are reserved for semantic state.

## 3. Typography

| Level | Size | Weight | Line height | Usage |
|---|---|---:|---:|---|
| Display | `clamp(3rem, 6.2vw, 6.6rem)` | 900 | 0.98 | 타이틀 |
| H1 | `clamp(2.25rem, 4.5vw, 4.7rem)` | 900 | 1.05 | 슬라이드 제목 |
| H2 | `clamp(1.45rem, 2.3vw, 2.35rem)` | 850 | 1.16 | 패널 제목 |
| Body large | `clamp(1.1rem, 1.65vw, 1.65rem)` | 650 | 1.5 | 핵심 설명 |
| Body | `clamp(0.95rem, 1.25vw, 1.2rem)` | 560 | 1.52 | 본문 |
| Caption | `clamp(0.72rem, 0.9vw, 0.9rem)` | 760 | 1.4 | 라벨 |

- Primary: `-apple-system`, `BlinkMacSystemFont`, `SF Pro Text`, `Pretendard`, `Segoe UI`, sans-serif
- Mono: `JetBrains Mono`, `SFMono-Regular`, `Menlo`, monospace
- Korean display copy uses `word-break: keep-all` and balanced wrapping.

## 4. Spacing & Layout

- Base unit: 4px
- Slide canvas: `100dvw × 100dvh`
- Desktop content width: 1280px
- Main slide padding: 48px to 72px
- Breakpoints: 720px and 1100px
- Reusable spacing tokens: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80px
- Desktop layouts use asymmetric 12-column or purpose-built grids. Mobile collapses to one column.

## 5. Components

### Slide Shell

- Structure: `section.slide > .slide-inner` with semantic heading and content groups
- States: inactive, active, overview, print
- Accessibility: one active slide, `aria-hidden` sync, keyboard and swipe navigation
- Motion: active slide fades and rises; reduced motion removes translation

### Concept Panel

- Structure: label, title, short explanation
- Variants: default, blue, green, amber, red, dark
- Spacing: 20px or 24px internal padding
- States: static only
- Accessibility: semantic headings and sufficient contrast

### Agent Stack

- Structure: stacked layers connected by a central execution rail
- Variants: title stack, three-tier maturity stack
- Motion: the active slide enters as one stable reading surface

### Bounded Loop

- Structure: goal, observe, decide, authorize, act, verify, stop or retry
- States: normal path, retry path, human handoff
- Accessibility: DOM order matches the visual direction
- Motion: no internal animation; the complete loop remains visible for explanation

### Deck Controls

- Structure: previous, notes, overview, next
- States: default, hover, active, focus, disabled
- Accessibility: real buttons, visible focus, keyboard shortcuts, live counter

### Notes Drawer

- Structure: heading and current speaker note
- States: closed, open
- Accessibility: `aria-live`, Escape closes

## 6. Motion & Interaction

- Micro: 120ms ease-out for button feedback
- Standard: 240ms ease-in-out for notes and overview
- Emphasis: 460ms cubic-bezier(0.16, 1, 0.3, 1) for active-slide entry
- Only opacity and transform animate.
- Motion communicates slide activation, reading order, or an explicit control state.
- `prefers-reduced-motion: reduce` disables all nonessential motion.

## 7. Depth & Surface

Strategy: mixed, with subtle blue-tinted shadows and one-pixel borders.

- Panels: `1px solid var(--line)`
- Resting shadow: `0 16px 42px rgba(24, 74, 128, 0.08)`
- Elevated shadow: `0 28px 80px rgba(12, 52, 96, 0.14)`
- Radius rule: panels 20px, compact controls 12px, state chips full-pill

## 8. Accessibility Constraints & Accepted Debt

### Constraints

- WCAG 2.2 AA contrast target
- Full keyboard navigation
- Touch swipe support
- Visible focus on every control
- `prefers-reduced-motion` support
- Natural Korean line wrapping at 1920×1080, 1280×720, 768×1024, and 375×812
- Mobile slides may scroll vertically when content cannot fit without reducing text below the scale

### Inclusive personas

- 강의실 뒤쪽에서 프로젝터를 보는 참가자: 큰 핵심 문장과 높은 대비 필요
- 에이전트를 처음 접하는 개발자: 한 슬라이드에 한 개념, 용어 정의 필요
- 키보드로 발표를 진행하는 강사: 모든 기능을 키보드로 조작 가능해야 함
- 모션 민감 사용자: 자동 반복 모션 없이 정적인 대체 상태 제공

### Accepted Debt

| Item | Location | Why accepted | Owner / Exit |
|---|---|---|---|
| 별도 발표자 팝업 없음 | `agentmake/index.html` | 기존 SBTI 런타임과 동일한 노트 서랍으로 충분 | 실제 강의 리허설에서 필요할 때 추가 |
