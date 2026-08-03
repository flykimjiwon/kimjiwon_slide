# SBTI4 Visual Options Design System

## 1. Atmosphere & Identity

어두운 관제실 안에서 친근한 픽셀 유령들이 기술 개념을 직접 작업해 보이는 선택 갤러리다. 시그니처는 짙은 네이비 격자 위의 청록 네온 연결선과, 역할마다 다른 색을 가진 둥근 유령 캐릭터다. 새 그림은 설명문을 이미지 안에 넣지 않고 도구·문서·연결 관계만으로 의미가 읽혀야 한다.

## 2. Color

| Role | Token | Value | Usage |
| --- | --- | --- | --- |
| Page surface | `--navy` | `#07101f` | 본문 배경, 선택 카드의 어두운 글자 |
| Raised surface | `--navy2` | `#0d1930` | 안내·보조 패널 |
| Card surface | implicit | `#0b172a` | 선택 카드 |
| Visual surface | implicit | `#050c18` | 이미지 프레임 |
| Text primary | `--ink` | `#eef6ff` | 제목·주요 텍스트 |
| Text secondary | `--muted` | `#8fa5c2` | 설명·메타데이터 |
| Border | `--line` | `#19345d` | 구획선·기본 경계 |
| Accent | `--cyan` | `#18d7f2` | 선택·핵심 연결·포커스 |
| Supporting blue | `--blue` | `#1677ff` | 이미지 내 보조 네온 |
| Attention | `--yellow` | `#ffd84a` | 안내·중요 라벨 |
| Success | `--green` | `#4ce58a` | 선택 완료·추가 완료 |
| Character accent | `--pink` | `#ff6f91` | 유령 역할 구분 |

이미지 팔레트는 네이비, 청록, 전기 파랑, 보라, 초록, 노랑·주황, 코럴 핑크, 흰색만 쓴다. 본문에서는 청록을 상호작용·선택 의미에 우선 사용한다.

## 3. Typography

| Level | Size | Weight | Line height | Usage |
| --- | --- | --- | --- | --- |
| Display | `clamp(38px, 7vw, 82px)` | 700 | 1 | 페이지 제목 |
| Section title | `clamp(25px, 4vw, 40px)` | 700 | inherited | 장면 제목 |
| Card title | `16px` | 700 | inherited | 시안 이름 |
| Lead | `18px` | 400 | 1.55 | 페이지 설명 |
| Body small | `13px` | 400 | inherited | 시안 설명 |
| Caption | `12px` | 700 | inherited | 칩·상태 |
| Overline | `13px` | 700 | 1.2 | 영문 상단 라벨 |

- Primary: `Pretendard, "Noto Sans KR", sans-serif`
- Mono: `"JetBrains Mono", monospace`
- 한국어 문장은 `word-break: keep-all`을 우선하고, 모바일에서 한 글자만 고립되는 줄바꿈을 허용하지 않는다.

## 4. Spacing & Layout

- 기본 단위는 4px이며, 기존 화면의 8·12·16·20·24·32px 리듬을 우선한다.
- 최대 콘텐츠 폭은 1180px, 데스크톱 바깥 여백은 20px, 모바일은 12px이다.
- 비교 시안은 데스크톱 2열, 720px 이하 1열이다.
- `FeaturedScene`은 항상 1열 전체 폭이며 다른 비교 시안보다 먼저 온다.
- 이미지 프레임은 데스크톱 16:9, 모바일 16:10을 유지하고 `object-fit: cover`로 채운다.

## 5. Components

### FeaturedScene

- **Structure**: `section.group > header.group-head + figure.feature-card > .visual + figcaption.meta`
- **Variants**: 현재는 `NEW` 한 종류만 사용한다.
- **Spacing**: 기존 `group`, `visual`, `meta`, `key` 리듬을 그대로 재사용한다.
- **States**: 비상호작용 콘텐츠이므로 hover·active·선택 상태를 만들지 않는다.
- **Accessibility**: 의미를 모두 설명하는 한국어 `alt`; 이미지와 캡션을 `figure`/`figcaption`으로 연결한다.
- **Motion**: 없음.
- **Layout**: 전체 폭 stack. 갤러리의 첫 콘텐츠로 배치한다.

### OptionCard

- **Structure**: `label.option > input[type=radio] + .visual + .meta`
- **Variants**: 현재안, 신규 후보, 선택됨.
- **States**: default, hover, keyboard focus, selected. 비활성·loading·error 상태는 이 정적 선택 갤러리에 필요하지 않다.
- **Accessibility**: 라벨 전체가 라디오의 클릭 영역이며, 키보드 포커스 링과 의미 있는 이미지 `alt`를 제공한다.
- **Motion**: hover 시 `transform`만 180ms; reduced-motion에서는 제거한다.
- **Layout**: 데스크톱 2열 grid, 모바일 1열 stack.

### SelectionSummary

- **Structure**: sticky `aside` 안의 장면별 `.pick-chip`.
- **States**: 선택값 변경 시 해당 굵은 텍스트와 카드 상태 문구를 즉시 갱신한다.
- **Accessibility**: 선택 입력과 동일한 읽기 순서를 유지한다.
- **Motion**: 없음.
- **Layout**: 가로 overflow가 가능한 cluster.

### RightsCredit

- **Structure**: `footer .rights-note` 안에 제작·AI 보조·인용·상표 경계를 짧은 문단으로 묶는다.
- **States**: 정적 정보. 링크를 추가하는 경우에만 default·hover·focus 상태를 제공한다.
- **Accessibility**: `aria-label`이 있는 footer landmark와 충분한 대비, 모바일 자연 줄바꿈을 유지한다.
- **Motion**: 없음.
- **Layout**: 데스크톱 2열 정보 grid, 720px 이하 1열 stack.

## 6. Motion & Interaction

| Type | Duration | Easing | Usage |
| --- | --- | --- | --- |
| Micro | `180ms` | `ease` | 선택 카드 hover와 경계 변화 |

- 움직임은 선택 가능성 또는 선택 상태만 설명한다.
- 비상호작용 `FeaturedScene`에는 hover 이동을 넣지 않는다.
- `prefers-reduced-motion: reduce`에서는 smooth scroll과 카드 transition을 제거한다.

## 7. Depth & Surface

전략은 mixed다. 카드는 얇은 파란 경계와 네이비 tonal shift로 분리하고, 선택된 카드에만 청록 외곽광과 깊은 그림자를 준다. 생성 이미지는 배경 격자, 픽셀 림 라이트, 제한된 네온 광으로 깊이를 만들며 UI 카드 그림자를 이미지 안에 흉내 내지 않는다.

## 8. Accessibility Constraints & Accepted Debt

### Constraints

- WCAG 2.2 AA를 목표로 하며 모든 라디오 선택은 키보드로 도달 가능해야 한다.
- 의미 있는 이미지는 장면의 핵심 관계를 설명하는 한국어 대체 텍스트를 가진다.
- 375px에서 가로 스크롤 없이 한 열로 읽혀야 한다.
- 200% 확대에서도 제목·설명·상태가 겹치거나 잘리지 않아야 한다.
- 장식적 움직임을 넣지 않고 reduced-motion을 존중한다.

### Accepted Debt

| Item | Location | Why accepted | Owner / Exit |
| --- | --- | --- | --- |
| 없음 | — | — | — |

### Observed legacy inconsistency

- 기존 단일 HTML은 일부 보조색과 간격을 인라인 값으로 보유한다. 이번 변경에서 새 패턴은 기존 의미 토큰만 재사용하며, 별도 사용자 승인 없이 이 불일치를 accepted debt로 승격하지 않는다.
