# EASY AI 정본·시인성 삽화 갤러리 Design System

상위 디자인 시스템: [`../../DESIGN.md`](../../DESIGN.md), [`../../visual-options/DESIGN.md`](../../visual-options/DESIGN.md). 이 폴더는 이전 후보 팩을 교체하지 않고, 라이브 [`/sbti4`](https://kimjiwon-slide.vercel.app/sbti4) 표지 언어의 픽셀 270점과 같은 개념 관계를 더 빠르게 읽게 하는 시인성 우선 270점을 함께 보관한다. 30개 개념마다 정본·비유 A·비유 B를 가로·정사각·세로로 제공하므로, 두 처리 방식은 각각 270점, 전체는 540점이다.

## 1. Atmosphere & Identity

두 처리 방식은 같은 개념·동일한 비유 A/B·동일한 세 비율을 공유한다. 픽셀 구성도는 큰 정사각 픽셀을 쌓은 친근한 작업자 유령과 짙은 남색 도트 격자를 유지한다. 시인성 우선 다이어그램은 유령 실루엣을 둥근 사람 노드와 사물별 선명한 아이콘으로 바꾸고, 밝은 표면·얇은 화살표·넉넉한 여백으로 관계를 먼저 읽게 한다. 모든 장면은 한 개의 기술 개념을 작은 교육용 도식처럼 읽히게 하며, 확장 개념은 `MCP · PROTOCOL`, `AGENT SYSTEM`, `SAFETY · EVAL`, `KNOWLEDGE`, `CONTEXT`, `RUNTIME`, `PIXEL CREW · REDRAW`로 라벨링해 비교한다.

- **기억할 장면**: 픽셀판은 청록 신호선이 체크 카드·도구·파란 제어 코어를 잇는 굵은 회로다. 시인성판은 같은 가방·나침반·선반·검문소 관계를 둥근 카드와 부드러운 연결 화살표로 보여 준다.
- **사용자**: 삽화를 슬라이드에 채택하기 전에 비율과 개념을 빠르게 비교하는 발표자료 작성자
- **안티 레퍼런스**: 유광 3D, 사진 질감, 과한 블러, 촘촘한 네온 UI, 이미지 안 텍스트. 픽셀판은 부드러운 모서리를 쓰지 않으며, 시인성판은 관계를 구분하는 정도의 둥근 모서리만 쓴다.
- **재생성 원본**: `metaphor-catalogue.mjs`의 개념별 A·B 비유와 `render-semantic-pixel-variants.mjs`의 단색 사각형 렌더러가 픽셀 보강 180개를 재현한다. `clarity-catalogue.mjs`와 `render-clarity-diagrams.mjs`는 정본·비유 A·비유 B의 시인성 우선 270개를 재현하며, `clarity-tokens.mjs`가 해당 다이어그램의 색상 원본이다. `pixel-tokens.mjs`와 `semantic-glyphs.mjs`는 픽셀판의 팔레트와 사물 실루엣 원본이다.

## 2. Color

| Token | Value | Usage |
| --- | --- | --- |
| `--canvas` | `#101722` | 실제 삽화의 평평한 남색 바탕 |
| `--navy` | `#07101f` | 갤러리 바탕 |
| `--navy-2` | `#0d1930` | 안내·카드 표면 |
| `--grid-dot` | `#123166` | 큰 정사각 도트 격자 |
| `--line` | `#19345d` | 카드·모달 경계 |
| `--ink` | `#eef6ff` | 제목·주요 텍스트 |
| `--muted` | `#8fa5c2` | 설명·메타 |
| `--cyan` | `#18d7f2` | 연결선·포커스·선택 |
| `--blue` | `#1677ff` | 제어 코어·보조 신호 |
| `--yellow` | `#ffd84a` | 헬멧·도구 포인트 |
| `--pink` | `#ff6f91` | 볼·역할 포인트 |
| `--white` | `#f8fafc` | 눈·문서 카드 |
| `--art-shadow` | `#07111f` | 삽화의 계단 그림자 |
| `--art-panel` | `#0d1f3b` | 삽화 안쪽 패널 면 |
| `--sky` | `#6ee7ff` | 유령 몸체·밝은 신호 |
| `--blue-deep` | `#0d5fbd` | 제어 코어의 안쪽 사각층 |
| `--green` | `#4ade80` | 검증·권한 통과 표시 |
| `--coral` | `#ff8787` | 오류·차단 위험 표시 |
| `--art-ink` | `#1b2733` | 유령 눈·삽화의 가장 짙은 세부 |
| `clarityColors.surface` | `#F3F8FA` | 시인성 우선 다이어그램의 밝은 배경 |
| `clarityColors.ink` | `#173042` | 시인성 우선 다이어그램의 선명한 윤곽 |
| `clarityColors.cyan` | `#19BFD0` | 시인성 우선 다이어그램의 연결 화살표 |
| `clarityColors.line` | `#B9D2D9` | 시인성 우선 다이어그램의 카드 경계 |
| `--shadow` | `rgba(0,0,0,.36)` | 갤러리 모달만의 실제 깊이 그림자 |
| `--focus-ring` | `rgba(24,215,242,.18)` | 클릭 가능한 카드 hover 외곽광 |
| `--dialog-backdrop` | `rgba(1,5,13,.76)` | 모달 뒤 실제 차광층 |

갤러리는 `--*` 토큰만 사용한다. `art-*`와 `--sky`·`--blue-deep`·`--green`·`--coral`은 PNG 전용의 단색 픽셀 토큰이고, `clarityColors`와 `clarityAccents`는 시인성 PNG 전용 토큰이다. 세 alpha 토큰은 실제 떠 있는 UI 상태에만 쓴다. 픽셀판은 단색 사각형만으로, 시인성판은 평평한 벡터 도형과 관계 화살표로 렌더링한다.

## 3. Typography

| Token | Value | Usage |
| --- | --- | --- |
| `--font-sans` | `Pretendard, "Noto Sans KR", system-ui, sans-serif` | 한국어 본문 |
| `--font-mono` | `"JetBrains Mono", ui-monospace, monospace` | 비율·상태 |
| `--text-display` | `clamp(32px, 6vw, 64px)` / 800 | 페이지 제목 |
| `--text-section` | `clamp(21px, 3vw, 30px)` / 800 | 개념 제목 |
| `--text-body` | `16px` / 1.65 | 설명 |
| `--text-meta` | `13px` / 1.45 | 비율·상태 |

한글은 `word-break: keep-all`을 우선하며, 이미지의 의미를 제목·설명·대체 텍스트에 중복해 제공한다.

## 4. Spacing & Layout

- 기본 단위는 4px: `--space-1`(4px), `--space-2`(8px), `--space-3`(12px), `--space-4`(16px), `--space-5`(20px), `--space-6`(24px), `--space-8`(32px), `--space-10`(40px), `--space-12`(48px)이다.
- 콘텐츠 최대폭은 1180px, 데스크톱 바깥 여백은 20px, 모바일은 12px이다.
- `ConceptCard`는 960px 이상에서 2열, 그 아래는 1열이다. 각 카드 안에는 정본·비유 A·비유 B의 픽셀·시인성 `VariantBlock` 여섯 묶음이 있고, 내부 비율 카드 3개는 충분한 식별 폭을 확보한 뒤 모바일에서 1열로 전환한다. 처리·버전·비율 필터 결과가 한 장이면 그 카드가 전체 폭을 써서 관계가 축소되지 않게 한다.
- 원본 PNG는 `wide` 1672×941, `square` 941×941, `portrait` 753×941로 고정한다. CSS 미디어 영역도 각각 정확히 `1672 / 941`, `1`, `753 / 941`를 사용해 비율을 근사하거나 가장자리 픽셀을 자르지 않는다.

## 5. Components

### RatioFilter

- **Structure**: `nav.filterbar > button.filter`.
- **States**: default, hover, focus-visible, selected (`aria-pressed=true`).
- **Accessibility**: 현재 결과 수를 `aria-live`로 알리고 버튼 이름에 결과 수를 제공한다.
- **Motion**: 160ms `transform`과 `border-color`만 사용하며 reduced-motion에서는 즉시 전환한다.

### VersionFilter

- **Structure**: `nav.filterbar > button.filter[data-version-filter]`.
- **States**: 전체, 정본, 비유 A, 비유 B. 비율 필터와 독립적으로 조합한다.
- **Accessibility**: 두 필터의 선택 상태는 각각 `aria-pressed`로 제공하고, 결과 수는 하나의 `aria-live` 문장으로 갱신한다.

### TreatmentFilter

- **Structure**: `nav.filterbar > button.filter[data-treatment-filter]`.
- **States**: 전체 그림체, 픽셀, 시인성 우선. 버전·비율 필터와 독립적으로 조합한다.
- **Accessibility**: `?treatment=clarity` URL로 시인성 우선 270점을 바로 열 수 있으며, 현재 처리 방식과 결과 수를 `aria-live`로 함께 알린다.

### ConceptCard · VariantBlock

- **Structure**: `article.concept-card > header + .variant-list > section.variant-block > header + .asset-list`.
- **States**: 필터로 내부 카드가 모두 감춰지면 `VariantBlock`과 `ConceptCard`를 함께 `hidden` 처리한다.
- **Accessibility**: 각 묶음은 고유한 `h2`로 시작한다.
- **Layout**: 큰 화면 2열 concept grid, 내부 3열 asset grid; 모바일 1열. 버전 또는 비율 필터로 카드가 하나만 남으면 `asset-list-single`으로 확장한다. 모바일에서도 미디어를 정사각 썸네일로 강제하지 않고 각 원본 비율 전체를 보인다.

### AssetCard

- **Structure**: `button.asset-card > figure > .asset-media > img + figcaption`.
- **States**: default, hover, focus-visible; 클릭 시 `PreviewDialog`를 연다. 픽셀 카드만 `image-rendering: pixelated`를 사용하고 시인성 카드는 원래의 부드러운 윤곽을 보존한다.
- **Accessibility**: 실제 장면 관계를 설명한 한국어 `alt`와 확대 목적의 접근성 이름을 제공한다.
- **Motion**: hover에만 160ms `translateY`를 쓰며 장식 애니메이션은 없다.

### PreviewDialog

- **Structure**: `dialog.preview-dialog > .preview-shell > header + figure + .preview-actions`.
- **States**: closed, open, previous/next, keyboard focus.
- **Accessibility**: `showModal()`, Escape, 닫기, 좌·우 화살표, 포커스 반환을 지원한다.
- **Motion**: 실제 열림 상태 변화에만 160ms opacity/transform을 사용한다.

## 6. Motion & Interaction

| Type | Duration | Easing | Usage |
| --- | --- | --- | --- |
| Micro | `160ms` | `ease-out` | 필터·카드 피드백 |
| Dialog | `160ms` | `ease-out` | 실제 미리보기 전환 |

`prefers-reduced-motion: reduce`에서 모든 전환을 제거한다. 비상호작용 그림은 움직이지 않는다.

## 7. Depth & Surface

갤러리 카드에는 `--line` 경계와 `--navy-2` tonal shift만 쓴다. 얇은 청록 외곽광은 선택·hover·focus에만 허용된다. 깊은 그림자는 실제로 전면에 뜨는 `PreviewDialog`에만 사용한다. 삽화 내부에는 갤러리 UI의 그림자·유리 효과를 흉내 내지 않는다.

## 8. Accessibility Constraints & Accepted Debt

### Constraints

- WCAG 2.2 AA를 목표로 하며 모든 제어는 키보드로 도달 가능해야 한다.
- 375px, 768px, 1280px과 200% 확대에서 가로 overflow·메타 잘림이 없어야 한다.
- 대비·관계·비율의 뜻을 색만으로 전달하지 않는다.
- 모든 PNG는 명확한 한국어 대체 텍스트를 갖는다.

### Accepted debt

| Item | Location | Reason / Exit |
| --- | --- | --- |
| 없음 | — | — |
