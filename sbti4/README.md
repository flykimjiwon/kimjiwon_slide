# SBTI4 복원·운영 안내

이 폴더가 SBTI4의 전체 정본입니다. 이후 세션에서 "SBTI4 풀받아", "SBTI4 전부 복원해", "발표자료 싹 다 받아"라고 하면 `origin/main`의 `sbti4/` 전체를 기준으로 가져옵니다.

## 정본 파일

- `index.html`: 실제 발표·배포용 최종 책자. 선택된 그림까지 data URI로 내장한 단일 HTML이라 이 파일 하나만으로 오프라인 실행할 수 있습니다.
- `visual-options/index.html`: 기존안과 신규안 총 16점을 비교하고 선택하는 갤러리입니다.
- `visual-options/*.png`: 표지·하네스·멀티에이전트·메모리별 신규 후보 3점씩, 총 12점입니다.
- `assets/ghost-*`: 갤러리의 기존안과 SBTI 유령 원본 자산입니다.
- `assets/*.jpg`: 제작 과정에서 만든 이전 콘셉트 후보와 보관용 이미지입니다.

## 현재 최종 선택

| 위치 | 선택안 | 그림 의미 |
| --- | --- | --- |
| 표지 | B 설계 테이블 | 역할이 다른 유령들이 한 도면을 함께 설계 |
| 하네스 | A 3단 검문 | 도구·보안·검증 게이트를 차례로 통과 |
| 멀티에이전트 | C 피드백 순환 | 계획→구현→검토 후 필요하면 다시 반복 |
| 메모리·LLM 위키 | A 위키 선반 | 검색·검증한 지식을 다음 세션용으로 축적 |

최종 선택 이미지는 `index.html` 안에 내장되어 있습니다. `visual-options/index.html`의 선택값은 브라우저 `localStorage`에도 저장되지만, 정본 판단은 위 표와 `index.html`을 우선합니다.

## 최신 전체 자료 받기

저장소 전체를 이미 받은 상태라면:

```bash
cd ~/kimjiwon_slide
git pull --ff-only origin main
open sbti4/index.html
```

SBTI4 폴더만 sparse clone으로 새로 받으려면:

```bash
git clone --filter=blob:none --sparse https://github.com/flykimjiwon/kimjiwon_slide.git
cd kimjiwon_slide
git sparse-checkout set sbti4
open sbti4/index.html
```

## 로컬 실행

```bash
open sbti4/index.html
open sbti4/visual-options/index.html
```

별도 빌드나 서버가 필요하지 않습니다. 배포 시에는 `index.html`만으로도 열리지만, 시안 재선택과 전체 자산 보존을 위해 Git에는 `sbti4/` 폴더 전체를 유지합니다.

## 수정 원칙

- 발표 정본은 항상 `index.html`입니다.
- 새 그림을 채택하면 이미지와 캡션을 함께 수정합니다.
- 최종 책자는 단일 파일·오프라인 실행을 유지합니다.
- 후보 이미지는 삭제하지 않고 `visual-options/` 또는 `assets/`에 보관합니다.
- SBTI4와 무관한 저장소 변경은 같은 커밋에 섞지 않습니다.
