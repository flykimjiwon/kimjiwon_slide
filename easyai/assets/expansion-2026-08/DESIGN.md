# Easy AI 확장 삽화 갤러리 Design System

상위 디자인 시스템: [`../../visual-options/DESIGN.md`](../../visual-options/DESIGN.md). 이 갤러리는 상위의 어두운 관제실·친근한 픽셀 유령 문법을 그대로 쓰며, 27개 후보를 빠르게 비교하고 확대하는 용도의 정적 자산 브라우저다.

## 1. Atmosphere & Identity

짙은 네이비 도트 격자 위에서 청록 신호가 9개 개념 묶음을 연결한다. 사용자는 카드의 비율 필터로 후보를 좁히고, 실제 PNG를 모달로 크게 본다. UI 자체는 정보를 정리하는 관제 패널이며, 삽화의 색·캐릭터가 주인공이다.

## 2. Color

상위 토큰 `--navy`, `--navy2`, `--ink`, `--muted`, `--line`, `--cyan`, `--blue`, `--yellow`, `--green`, `--pink`을 그대로 사용한다. 이 폴더에서만 필요한 의미 토큰은 다음과 같다.

| Token | Value | Usage |
| --- | --- | --- |
| `--card` | `#0b172a` | 개념 묶음과 후보 카드 표면 |
| `--visual` | `#050c18` | PNG 프레임 |
| `--grid-dot` | `#16427c` | 페이지 배경의 미세 격자 |
| `--cyan-glow` | `rgba(24, 215, 242, .18)` | 선택·hover의 얇은 외곽광 |
| `--shadow` | `rgba(0, 0, 0, .28)` | 실제 떠 있는 미리보기 모달 그림자 |

## 3. Typography

상위의 Display, Section title, Card title, Lead, Body small, Caption, Overline 스케일을 따른다. Primary는 `Pretendard, "Noto Sans KR", sans-serif`, Mono는 `"JetBrains Mono", monospace`다. 한국어는 `word-break: keep-all`을 우선하고, 카드 제목·비율·사용처는 짧은 의미 단위로만 줄바꿈한다.

## 4. Spacing & Layout

- 기본 단위는 4px이며 `--space-1`(4px)부터 `--space-12`(48px)까지의 4px 배수를 쓴다.
- 최대 콘텐츠 폭은 1180px, 가로 여백은 데스크톱 20px·모바일 12px이다.
- `ConceptCard`는 데스크톱에서 2열, 후보가 충분히 식별되는 폭을 보장하기 위해 900px 이하에서 1열이다.
- 내부 후보는 넓이·정사각·세로 원본 비율을 유지하며, 640px 이하에서 한 열로 내려간다.
- 375px과 200% 확대에서 수평 overflow가 없어야 한다.

## 5. Components

### RatioFilter

- **Structure**: `nav.filterbar > .filter-summary + [role=group] > button.filter`.
- **States**: default, hover, focus-visible, selected (`aria-pressed=true`).
- **Accessibility**: 현재 결과 수를 `aria-live`로 알리고, 버튼 이름에 비율과 수를 함께 둔다.
- **Motion**: 선택·hover에만 180ms 색/transform 전환. reduced-motion에서는 즉시 바뀐다.

### ConceptCard

- **Structure**: `article.concept-card > header.concept-head + .asset-list`.
- **States**: 기본 표면만 사용한다. 필터로 내부 후보가 없으면 `hidden` 처리한다.
- **Accessibility**: 각 개념은 heading으로 시작해 스크린리더가 9개 묶음을 구분한다.
- **Layout**: 2열 concept grid, 내부 3열 후보 grid; 비율 필터 상태에서는 한 후보를 이미지·메타 2열로 넓혀 보이고, 모바일에서는 모두 1열 목록으로 정리한다.

### AssetCard

- **Structure**: `button.asset-card > figure(grid) > .asset-media > img + figcaption.asset-meta`; media와 메타는 `figure`의 실제 grid item이다.
- **States**: default, hover, focus-visible. 클릭하면 `PreviewDialog`를 연다.
- **Accessibility**: 의미 있는 한국어 `alt`, 버튼의 확대 목적을 밝힌 accessible name, 명료한 포커스 링을 제공한다.
- **Motion**: hover 시 `transform`만 180ms, reduced-motion에서는 제거한다.

### PreviewDialog

- **Structure**: `dialog.preview-dialog > .preview-shell > header + figure + .preview-actions`.
- **States**: closed, open, previous/next enabled, keyboard focus.
- **Accessibility**: `showModal()`로 포커스를 가두고 Escape·닫기 버튼으로 종료한다. 좌/우 화살표는 현재 필터 결과 안에서만 이동한다.
- **Motion**: 모달은 실제 상태 변화이므로 180ms opacity/transform만 사용하며, reduced-motion에서는 전환하지 않는다.

## 6. Motion & Interaction

| Type | Duration | Easing | Usage |
| --- | --- | --- | --- |
| Micro | 180ms | ease | 필터·자산 카드의 hover/focus 반응 |
| Dialog | 180ms | ease-out | 이미지 확대가 열릴 때의 실제 상태 변화 |

장식 애니메이션은 넣지 않는다. `prefers-reduced-motion: reduce`에서는 모든 전환과 smooth scroll을 끈다.

## 7. Depth & Surface

개념 묶음과 자산 카드는 `--line` 경계와 `--card` tonal shift로 분리한다. 청록 외곽광은 실제 선택·hover 피드백에만 사용한다. 깊은 그림자는 `PreviewDialog`처럼 다른 모든 내용을 가리는 실제 떠 있는 요소에만 사용한다.

## 8. Accessibility Constraints

- WCAG 2.2 AA를 목표로 한다.
- 모든 필터, 카드, 이전/다음/닫기 제어는 키보드로 도달 가능해야 한다.
- 모든 이미지에는 장면의 핵심 관계를 설명하는 한국어 alt가 있어야 한다.
- 375px, 768px, 1280px과 200% 확대에서 제목·메타·모달 제어가 겹치거나 잘리지 않아야 한다.
