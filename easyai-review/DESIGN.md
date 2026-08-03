# SBTI4 Chapter 4 Review Design System

## 1. Atmosphere & Identity

SBTI4의 밝고 단정한 기술 책자 분위기를 유지한다. 흰 종이 같은 카드, 차가운 회색 선, 짙은 남색 본문, 파란색 장 번호가 기본 인상이다. 이 비교본의 시그니처는 같은 높이와 같은 시작선을 가진 `기존 문구 / 추천 문구` 두 면이다. 시각적 장식보다 바뀐 이유와 문장 차이가 먼저 읽혀야 한다.

## 2. Color

### Palette

| Role | Token | Value | Usage |
| --- | --- | --- | --- |
| Page | `--bg` | `#fafafa` | 전체 배경 |
| Surface | `--surface` | `#ffffff` | 카드와 헤더 |
| Soft surface | `--soft` | `#f4f7fb` | 표 머리글, 보조 영역 |
| Recommended surface | `--recommend-soft` | `#eef7ff` | 추천 문구 배경 |
| Line | `--line` | `#e2e7ee` | 카드와 표 경계 |
| Text | `--text` | `#1a1a1a` | 본문 |
| Strong text | `--dark` | `#111827` | 제목 |
| Muted text | `--muted` | `#5f6672` | 설명과 메타데이터 |
| Accent | `--blue` | `#0066cc` | 장 번호, 링크, 포커스 |
| Info | `--cyan` | `#0ea5e9` | 쉬운 설명 |
| Success | `--green` | `#168345` | 유지 가능, 검증 완료 |
| Warning | `--orange` | `#c94d0b` | 표현 완화 |
| Critical | `--red` | `#c62828` | 반드시 수정 |
| Terminal | `--terminal` | `#232832` | 핵심 원칙 인용 |

### Rules

- 색상은 원본 `sbti4/index.html`의 암묵적 토큰을 기준으로 한다.
- 파란색은 링크, 포커스, 추천안의 구조 표시에만 쓴다.
- 상태 색은 배지와 좁은 왼쪽 선에만 사용하고 긴 본문 전체를 채우지 않는다.
- 새 색이 필요하면 이 표에 먼저 추가한다.

## 3. Typography

### Scale

| Level | Size | Weight | Line height | Usage |
| --- | --- | --- | --- | --- |
| Display | `clamp(2rem, 5vw, 3.5rem)` | 800 | 1.08 | 페이지 제목 |
| H1 | `clamp(1.55rem, 3vw, 2.25rem)` | 800 | 1.2 | 장 제목 |
| H2 | `1.25rem` | 800 | 1.35 | 비교 항목 제목 |
| H3 | `1rem` | 800 | 1.4 | 좌우 열 제목 |
| Body large | `1.0625rem` | 500 | 1.75 | 도입문 |
| Body | `1rem` | 400 | 1.75 | 비교 문구 |
| Body small | `0.875rem` | 500 | 1.6 | 수정 이유, 출처 |
| Caption | `0.75rem` | 700 | 1.4 | 번호, 상태 배지 |

### Font Stack

- Primary: `-apple-system, BlinkMacSystemFont, "SF Pro Text", "Pretendard", "Segoe UI", sans-serif`
- Mono: `"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace`
- 숫자와 영문 패턴명에는 `font-variant-numeric: tabular-nums`를 쓴다.

### Rules

- 원본의 시스템 폰트 조합을 유지한다.
- 본문은 14px 아래로 내리지 않는다.
- 한국어 제목은 `text-wrap: balance`, 본문은 `text-wrap: pretty`를 사용한다.

## 4. Spacing & Layout

### Base Unit

기본 단위는 4px다.

| Token | Value | Usage |
| --- | --- | --- |
| `--space-1` | `0.25rem` | 아이콘과 텍스트 |
| `--space-2` | `0.5rem` | 작은 인라인 간격 |
| `--space-3` | `0.75rem` | 배지와 설명 |
| `--space-4` | `1rem` | 카드 내부 최소 간격 |
| `--space-5` | `1.25rem` | 열 내부 간격 |
| `--space-6` | `1.5rem` | 카드 패딩 |
| `--space-8` | `2rem` | 카드 사이 |
| `--space-10` | `2.5rem` | 섹션 사이 |
| `--space-12` | `3rem` | 주요 구획 |
| `--space-16` | `4rem` | 페이지 상하 여백 |

### Grid

- 최대 본문 폭: `88rem`
- 비교 열: 넓은 화면에서 `minmax(0, 1fr) minmax(0, 1fr)`
- 비교 열 간격: `--space-4`
- 페이지 거터: `clamp(1rem, 3vw, 2.5rem)`
- 56rem 이하에서는 기존/추천을 한 열로 재배치한다.
- 32rem 이하에서는 요약 지표와 상단 작업 버튼도 한 열로 재배치한다.

### Scroll ownership

- 문서 전체가 유일한 세로 스크롤 소유자다.
- 상단 도구막대는 넓은 화면에서만 `position: sticky`다. 56rem 이하에서는 문서 흐름에 두어 세로 공간을 가리지 않는다.
- 표만 좁은 화면에서 가로 스크롤할 수 있다.

## 5. Components

### Review header

- **Structure**: `header > eyebrow + h1 + lead + summary metrics`
- **Variants**: 기본 한 가지
- **Spacing**: `--space-8`, `--space-12`
- **States**: 정적
- **Accessibility**: 한 페이지에 `h1` 하나, 요약 수치는 텍스트로도 설명
- **Motion**: 없음
- **Layout**: content-limiter와 intrinsic grid

### Review toolbar

- **Structure**: `nav > original link + filter buttons + copy button`
- **Variants**: 링크, 보조 버튼, 주요 버튼
- **Spacing**: `--space-2`, `--space-3`
- **States**: default, hover, active, focus-visible, disabled
- **Accessibility**: 실제 `a`와 `button`, 현재 필터에 `aria-pressed`
- **Motion**: 180ms 색·transform 전환, reduced motion에서 제거
- **Layout**: sticky cluster, 문서 스크롤

### Comparison row

- **Structure**: `article > header + .comparison-grid > before + after + rationale`
- **Variants**: critical, clarity, terminology, keep
- **Spacing**: `--space-4`, `--space-6`, `--space-8`
- **States**: default, filtered-hidden, copy-confirmed
- **Accessibility**: 각 행은 고유 제목을 가진 `article`; 삭제/추가 문구는 `del`과 `mark`로 표시
- **Motion**: 필터 변경 시 opacity 180ms, reduced motion에서 즉시 전환
- **Layout**: switcher; 넓은 화면 두 열, 56rem 이하 한 열

### Status badge

- **Structure**: `span` + 상태 아이콘 SVG + 라벨
- **Variants**: critical, clarity, terminology, keep
- **Spacing**: `--space-1`, `--space-2`
- **States**: 정적
- **Accessibility**: 색 외에 텍스트와 아이콘 모양으로 구분
- **Motion**: 없음
- **Layout**: cluster

### Source note

- **Structure**: `aside > h2 + ol > li > a`
- **Variants**: 공식 문서, 논문
- **Spacing**: `--space-3`, `--space-5`
- **States**: link default, hover, focus-visible
- **Accessibility**: 출처 이름이 링크 목적을 설명
- **Motion**: 없음
- **Layout**: content-limiter

### Comparison primitive showcase

- `showcase.html`이 배지 네 종류, 버튼 상태, 짧은/긴/깨지지 않는 문자열, 두 열/한 열 재배치를 확인하는 상태 하네스다.

## 6. Motion & Interaction

| Type | Duration | Easing | Usage |
| --- | --- | --- | --- |
| Micro | `120ms` | `ease-out` | 버튼 눌림 |
| Standard | `180ms` | `ease-in-out` | hover, filter |

- `transform`과 `opacity`만 애니메이션한다.
- `prefers-reduced-motion: reduce`에서는 전환과 부드러운 스크롤을 제거한다.
- 장식 애니메이션은 사용하지 않는다.

## 7. Depth & Surface

### Strategy

`mixed`: 원본처럼 얇은 테두리를 기본으로 하고, sticky toolbar에만 아주 약한 그림자를 허용한다.

| Level | Value | Usage |
| --- | --- | --- |
| Border | `1px solid var(--line)` | 카드와 표 |
| Sticky shadow | `0 8px 24px rgba(17, 24, 39, 0.08)` | 상단 도구막대 |

- 비교 카드 본문에는 그림자를 쓰지 않는다.
- 추천 열은 배경색과 왼쪽 파란 선으로 구분한다.

## 8. Accessibility Constraints & Accepted Debt

### Constraints

- 목표: WCAG 2.2 AA.
- 본문 대비 4.5:1, 큰 글자와 UI 경계 3:1 이상.
- 모든 링크와 버튼은 키보드로 접근 가능하고 `:focus-visible` 윤곽선이 있다.
- 375px에서 기본 문서에 가로 스크롤이 없어야 한다.
- 상태는 색상만으로 전달하지 않는다.

### Accepted Debt

| Item | Location | Why accepted | Owner / Exit |
| --- | --- | --- | --- |
| 없음 | - | - | - |
