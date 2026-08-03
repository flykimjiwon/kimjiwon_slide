# 이미지 제작 이력 (PROVENANCE)

이 자료는 김지원이 업무 외 개인 시간에 기획·제작한 개인 저작물입니다.
아래는 본문에 쓰인 이미지의 제작 이력이며, **분쟁 시 "언제 어떻게 만들었는지"를 보이기 위한 기록**입니다.

- 정리일: 2026-08-03
- 대상: `easyai/assets/`, `easyai/visual-options/`, `easyai/assets/expansion-2026-08/`

---

## 1. 제작 이력이 파일 안에 남아 있는 것 (C2PA)

아래 파일들은 이미지 내부에 **C2PA(Content Credentials)** 서명이 들어 있어, 별도 기록 없이도
생성 도구와 시점을 파일 자체에서 확인할 수 있습니다.

| 묶음 | 파일 수 | 확인 방법 |
|---|---|---|
| `visual-options/*.png` (표지·하네스·멀티·메모리 후보 + MCP·A2A v1~v3) | 14+ | 파일 바이너리에 `jumb`/`c2pa` 청크 존재 |
| `assets/expansion-2026-08/*.png` (9개념 × 가로·정사각·세로 = 27점) | 27 | 동일 |

확인 명령:

```bash
python3 - <<'PY'
import glob
for p in sorted(glob.glob('easyai/**/*.png', recursive=True)):
    d = open(p, 'rb').read(200000)
    print('있음' if (b'jumb' in d or b'c2pa' in d) else '없음', p)
PY
```

C2PA는 **제작 이력의 증거**이지 저작권 보증서가 아닙니다. 하단 권리 표시의
"AI 제작 보조" 문구는 그대로 유지합니다.

---

## 2. 제작 이력이 파일에 없는 것 — 여기 기록으로 대체

아래 4점은 메타데이터가 남아 있지 않습니다. 초기 제작분이라 C2PA가 붙기 전에 만들어졌습니다.

| 파일 | 쓰임 | 제작 |
|---|---|---|
| `assets/ghost-search-to-memory.jpg` | 6장 메모리·위키 삽화 | 2026-07 · OpenAI 이미지 생성 도구 보조 · 콘셉트/프롬프트/선별/편집 김지원 |
| `assets/harness-layers.jpg` | 하네스 층 구조 초기안 (현재 미사용) | 2026-07 · 동일 |
| `assets/harness-vehicle.jpg` | 하네스 운전 비유 초기안 (현재 미사용) | 2026-07 · 동일 |
| `assets/search-to-memory.jpg` | 검색→메모리 초기안 (현재 미사용) | 2026-07 · 동일 |

> 위 4점 중 현재 본문에 실려 있는 것은 `ghost-search-to-memory.jpg` 하나이며,
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
