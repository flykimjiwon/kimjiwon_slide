# EASY AI 정본 픽셀 삽화 갤러리 Design System

상위 디자인 시스템: [`../../DESIGN.md`](../../DESIGN.md), [`../../visual-options/DESIGN.md`](../../visual-options/DESIGN.md). 이 폴더는 이전 후보 팩을 교체하지 않고, 라이브 [`/sbti4`](https://kimjiwon-slide.vercel.app/sbti4) 표지의 픽셀 언어에 맞춰 새로 만든 정본 27점을 보관한다.

## 1. Atmosphere & Identity

라이브 표지의 규칙은 유광·입체 게임 렌더가 아니라, 큰 정사각 픽셀을 쌓은 친근한 작업자 유령과 짙은 남색 도트 격자다. 모든 장면은 한 개의 기술 개념을 작은 교육용 도식처럼 읽히게 하며, 유령·카드·도구·신호선이 단순한 관계만 보여 준다.

- **기억할 장면**: 청록 신호선이 체크 카드·도구·파란 제어 코어를 잇는 굵은 픽셀 회로
- **사용자**: 삽화를 슬라이드에 채택하기 전에 비율과 개념을 빠르게 비교하는 발표자료 작성자
- **안티 레퍼런스**: 부드러운 모서리, 유광 3D, 블러·그라데이션, 촘촘한 네온 UI, 이미지 안 텍스트

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

이미지와 갤러리 모두 위 토큰만 사용한다. `--canvas`에는 그라데이션·광택·안개를 추가하지 않으며, 최종 PNG는 단색 사각형만으로 렌더링한다.

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
- `ConceptCard`는 960px 이상에서 2열, 그 아래는 1열이다. 내부 비율 카드 3개는 충분한 식별 폭을 확보한 뒤 모바일에서 1열로 전환한다.
- 원본 PNG는 `wide` 1672×941, `square` 941×941, `portrait` 753×941로 고정한다. 세로 원본의 여백은 픽셀을 찌그러뜨리지 않고 4:5 캔버스로 맞춘 결과다.

## 5. Components

### RatioFilter

- **Structure**: `nav.filterbar > button.filter`.
- **States**: default, hover, focus-visible, selected (`aria-pressed=true`).
- **Accessibility**: 현재 결과 수를 `aria-live`로 알리고 버튼 이름에 결과 수를 제공한다.
- **Motion**: 160ms `transform`과 `border-color`만 사용하며 reduced-motion에서는 즉시 전환한다.

### ConceptCard

- **Structure**: `article.concept-card > header + .asset-list`.
- **States**: 필터로 내부 카드가 모두 감춰지면 `hidden` 처리한다.
- **Accessibility**: 각 묶음은 고유한 `h2`로 시작한다.
- **Layout**: 큰 화면 2열 concept grid, 내부 3열 asset grid; 모바일 1열.

### AssetCard

- **Structure**: `button.asset-card > figure > .asset-media > img + figcaption`.
- **States**: default, hover, focus-visible; 클릭 시 `PreviewDialog`를 연다.
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
