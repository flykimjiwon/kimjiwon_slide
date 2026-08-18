# SBTI2 Illustration Gallery Design System

## 1. Atmosphere & Identity

SBTI2의 어두운 제품 슬라이드를 확장한 조용한 이미지 선택 콘솔입니다. 핵심 시그니처는 한 카드 안에서 원본과 투명 PNG를 같은 크기로 나란히 보여주는 2단 비교면이며, 장식보다 이미지 판별과 다운로드 속도를 우선합니다.

## 2. Color

| Role | Token | Value | Usage |
|---|---|---:|---|
| Background | `--bg` | `#0b1020` | 페이지 배경 |
| Surface | `--surface` | `#111827` | 카드, 필터 바 |
| Elevated | `--surface-elevated` | `#172033` | 모달, 강조 카드 |
| Muted surface | `--surface-muted` | `#0f172a` | 이미지 프레임 |
| Text primary | `--text` | `#f8fbff` | 제목, 본문 |
| Text secondary | `--muted` | `#b6c2d4` | 설명, 메타데이터 |
| Border | `--line` | `#263244` | 카드와 구분선 |
| Accent | `--accent` | `#0a84ff` | 선택 상태, 링크, 포커스 |
| Accent hover | `--accent-hover` | `#38bdf8` | 호버와 보조 강조 |
| Success | `--success` | `#34d399` | 투명 PNG 표식 |
| Warning | `--warning` | `#fbbf24` | 픽셀크루 표식 |
| Checker A | `--checker-a` | `#1c2638` | 투명 배경 격자 |
| Checker B | `--checker-b` | `#26344a` | 투명 배경 격자 |
| Overlay | `--overlay` | `rgb(2 6 23 / 0.9)` | 전체화면 모달 |

색상은 이미지 스타일을 가리지 않도록 네이비 계열을 유지합니다. `--accent`는 상호작용과 현재 선택에만 사용합니다.

## 3. Typography

| Level | Size | Weight | Line height | Usage |
|---|---:|---:|---:|---|
| Display | `clamp(2rem, 5vw, 4.5rem)` | 850 | 1.05 | 페이지 제목 |
| H2 | `clamp(1.5rem, 3vw, 2.5rem)` | 850 | 1.15 | 페이지 그룹 제목 |
| H3 | `1.125rem` | 800 | 1.35 | 스타일 카드 제목 |
| Body | `1rem` | 500 | 1.6 | 설명 |
| Small | `0.875rem` | 650 | 1.5 | 메타데이터, 버튼 |
| Label | `0.75rem` | 800 | 1.3 | 배지, 오버라인 |

- Primary: `-apple-system, BlinkMacSystemFont, "SF Pro Text", "Pretendard", "Segoe UI", sans-serif`
- Mono: `"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace`
- 한글 제목과 버튼은 `word-break: keep-all`을 기본으로 합니다.

## 4. Spacing & Layout

기본 단위는 4px입니다.

| Token | Value | Usage |
|---|---:|---|
| `--space-1` | 4px | 미세 간격 |
| `--space-2` | 8px | 인라인 간격 |
| `--space-3` | 12px | 배지, 버튼 내부 |
| `--space-4` | 16px | 카드 내부 |
| `--space-6` | 24px | 카드와 그룹 간격 |
| `--space-8` | 32px | 섹션 내부 |
| `--space-12` | 48px | 섹션 간격 |
| `--space-16` | 64px | 페이지 상하 여백 |

- 최대 콘텐츠 폭: 1440px
- 카드 그리드: 데스크톱 3열, 태블릿 2열, 모바일 1열
- 카드 안 비교면: 데스크톱 2열, 760px 이하 1열
- 기본 이미지 비율: 1672:941
- 주요 콘텐츠에는 가로 스크롤을 만들지 않습니다.

## 5. Components

### FilterBar
- **Structure**: 의미별 `fieldset`과 `button` 그룹
- **Variants**: 페이지 필터, 스타일 필터
- **States**: default, hover, active (`aria-pressed=true`), focus-visible
- **Accessibility**: 필터 목적을 `legend`로 제공하고 키보드로 모두 접근 가능
- **Motion**: 색과 테두리만 140ms 전환

### PageSection
- **Structure**: 페이지 번호, 제목, 핵심 설명, AssetCard 3개
- **Layout**: 3열 반응형 grid
- **States**: 필터 제외 시 `hidden`

### AssetCard
- **Structure**: 스타일 헤더, 원본 PreviewPane, 투명 PreviewPane, 다운로드 링크
- **Variants**: pixelcrew, ghost, concept
- **States**: default, hover, focus-within
- **Accessibility**: 각 이미지에 페이지·스타일·원본/투명 여부가 포함된 대체 텍스트

### PreviewPane
- **Structure**: 라벨과 실제 `img` 버튼
- **Variants**: original, transparent-checker
- **States**: default, hover, focus-visible
- **Layout**: 고정 aspect-ratio로 CLS 방지

### ImageModal
- **Structure**: `dialog`, 닫기 버튼, 전체 이미지, 설명, 원본 파일 링크
- **States**: closed, open, keyboard focus, loading
- **Accessibility**: `Esc` 닫기, 배경 클릭 닫기, 포커스 복귀, 이전·다음 방향키 탐색
- **Motion**: 열림·닫힘은 opacity와 transform만 사용하며 reduced-motion에서는 제거

## 6. Motion & Interaction

| Type | Duration | Easing | Usage |
|---|---:|---|---|
| Micro | 140ms | ease-out | 버튼, 카드 호버 |
| Standard | 220ms | ease-in-out | 모달 전환 |

- 상호작용을 설명하지 않는 장식 애니메이션은 사용하지 않습니다.
- `transform`, `opacity`, `color`, `border-color`만 전환합니다.
- `prefers-reduced-motion: reduce`에서는 비필수 전환을 제거합니다.

## 7. Depth & Surface

전략은 네이비 톤 변화와 얇은 경계선을 함께 쓰는 mixed 방식입니다.

- 카드: `--surface` + `--line` 경계
- 이미지 프레임: `--surface-muted`
- 모달: `--surface-elevated` + 강한 외곽 그림자
- 투명 미리보기: `--checker-a`, `--checker-b` 2색 격자
- 둥근 모서리는 카드 20px, 이미지 12px, 버튼 pill로 역할별 규칙을 고정합니다.

## 8. Accessibility Constraints & Accepted Debt

### Constraints
- WCAG 2.2 AA, 본문 대비 4.5:1 이상
- 모든 상호작용 요소에 `:focus-visible` 표시
- 키보드만으로 필터, 이미지 확대, 모달 닫기, 이미지 이동 가능
- 375px에서 자연스러운 한글 줄바꿈과 가로 스크롤 없음
- `prefers-reduced-motion` 존중
- 모든 이미지에 명시적 width·height와 대체 텍스트 제공

### Accepted Debt

| Item | Location | Why accepted | Owner / Exit |
|---|---|---|---|
| 없음 | - | - | - |
