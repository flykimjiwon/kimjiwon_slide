# 이미지 제작 이력 (PROVENANCE)

이 자료는 김지원이 업무 외 개인 시간에 기획·제작한 개인 저작물입니다.
아래는 본문에 쓰인 이미지의 제작 이력이며, **분쟁 시 "언제 어떻게 만들었는지"를 보이기 위한 기록**입니다.

- 정리일: 2026-08-03
- 대상: `easyai/assets/`, `easyai/visual-options/`, `easyai/assets/expansion-2026-08/`

---

## 1. 실측 현황 (2026-08-03)

이미지 47점 중 **C2PA(Content Credentials)가 남아 있는 것 25점 · 없는 것 22점**입니다.
저장소 루트에서 아래 스크립트로 언제든 다시 셀 수 있습니다.

```python
import glob
for p in sorted(glob.glob('easyai/**/*.png', recursive=True)) + sorted(glob.glob('easyai/**/*.jpg', recursive=True)):
    d = open(p, 'rb').read(200000)
    print('있음' if (b'jumb' in d or b'c2pa' in d) else '없음', p)
```

### 남아 있는 것 (25점)

| 묶음 | 수 |
|---|---|
| `visual-options/*.png` — 표지·하네스·멀티·메모리 후보 12점 + 지식시스템 + MCP·A2A v1~v3 | 16 |
| `assets/expansion-2026-08/*-wide.png` — 9개념 가로 버전 | 9 |

### 남아 있지 않은 것 (22점)

| 묶음 | 수 | 사유 |
|---|---|---|
| `assets/expansion-2026-08/*-portrait.png` · `*-square.png` | 18 | 가로 원본에서 비율을 바꿔 다시 저장하는 과정에서 메타데이터가 떨어져 나갔습니다. **같은 세션에서 만든 wide 9점에 C2PA가 남아 있어 제작 이력은 그쪽으로 확인됩니다.** |
| `assets/*.jpg` | 4 | 초기 제작분으로 C2PA가 붙기 전에 만들었습니다. 아래 표로 대체 기록합니다. |

C2PA는 **제작 이력의 증거**이지 저작권 보증서가 아닙니다. 하단 권리 표시의
"AI 제작 보조" 문구는 그대로 유지합니다.

---

## 2. 메타데이터가 없는 JPG 4점 — 기록으로 대체

| 파일 | 쓰임 | 제작 |
|---|---|---|
| `assets/ghost-search-to-memory.jpg` | 6장 메모리·위키 삽화 | 2026-07 · OpenAI 이미지 생성 도구 보조 · 콘셉트·프롬프트·선별·편집 김지원 |
| `assets/harness-layers.jpg` | 하네스 층 구조 초기안 (현재 미사용) | 2026-07 · 동일 |
| `assets/harness-vehicle.jpg` | 하네스 운전 비유 초기안 (현재 미사용) | 2026-07 · 동일 |
| `assets/search-to-memory.jpg` | 검색→메모리 초기안 (현재 미사용) | 2026-07 · 동일 |

> 이 중 현재 본문에 실려 있는 것은 `ghost-search-to-memory.jpg` 하나이며,
> 나머지 3점은 후보 보관분입니다. 후보는 삭제하지 않고 남겨 둡니다.

---

## 3. 외부에서 가져온 화면 캡처

2장 「LLM을 만나는 창구」의 4장은 **제품 화면 캡처**입니다. 생성 이미지가 아닙니다.

| 자리 | 원본 | 출처 |
|---|---|---|
| 웹 UI | `claude_web.png` | Claude 웹 화면 직접 캡처 |
| CLI | `codex_terminal.png` | OpenAI Codex 터미널 직접 캡처 |
| IDE 확장 | `glm_ide.png` | 코딩 확장 화면 직접 캡처 |
| 데스크톱 앱 | `claude_desktop.png` | Claude 데스크톱 직접 캡처 |

원본은 같은 저장소의 `sbti1/assets/`에 있습니다. 본문에는 폭 920px JPEG로 줄여 임베드했습니다.

각 화면에 나타나는 제품명·로고·UI는 해당 권리자에게 귀속되며, 본 자료는 제휴·후원·인증
관계를 표시하지 않습니다(하단 "상표·비제휴" 항목).

> **캡처 선별 기준** — 소속 조직명·업무 계정·사내 식별자가 찍힌 캡처는 사용하지 않습니다.
> 실제로 CLI 자리에 처음 골랐던 `claude_terminal.png`에 조직명과 업무 이메일이 노출돼 있어
> `codex_terminal.png`로 교체했습니다. 캡처를 새로 넣을 때 같은 기준을 적용하십시오.

---

## 4. 본문에 직접 그린 것

그림 1~10은 전부 **인라인 SVG**입니다. 외부 자산을 쓰지 않았고 `index.html` 안에 좌표로
들어 있어 별도 제작 이력이 필요 없습니다.
