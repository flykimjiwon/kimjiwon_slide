# SBTI 실습 — 코드베이스 탐색 과제

처음 보는 프로젝트를 **택가이 코드어시스턴트로 파악하는** 연습입니다.
가상의 사내 시스템 `roombook`(회의실 예약)이 들어 있습니다.
파일을 직접 뒤지지 말고 **AI에게 물어서** 답을 찾아보세요.

> 실습 환경은 사내망 온프레미스 모델(**Qwen3.6-35B**)입니다.
> 외부 프런티어 모델보다 한 번에 처리하는 양이 적으므로,
> **아래 「질문하는 방법」대로 좁게 나눠서 묻는 것이 이 실습의 핵심**입니다.

## 시작

```
cd roombook
techai
```

---

## 질문하는 방법 (이게 제일 중요합니다)

온프레미스 모델은 한 번에 프로젝트 전체를 읽지 못합니다.
**찾기 → 읽기 → 비교** 세 단계로 쪼개면 잘 답합니다.

### ❌ 이렇게 물으면 잘 안 됩니다

```
이 프로젝트 전체를 분석해서 문제점을 다 찾아줘
문서랑 코드가 다른 부분을 전부 알려줘
```

한 번에 너무 많은 파일을 읽어야 해서 답이 뭉개집니다.

### ⭕ 이렇게 물으면 잘 됩니다

**1단계 — 찾기 (검색부터 시킨다)**

```
MAX_HOURS 라는 문자열이 어느 파일에 있는지 찾아줘
"최대" 가 들어간 줄을 docs 폴더에서 찾아줘
```

**2단계 — 읽기 (파일 하나만 지정)**

```
backend/routes/middleware/time-range-check.js 파일을 읽고
예약 시간 제한이 몇 시간인지 알려줘
```

**3단계 — 비교 (둘만 놓고)**

```
방금 본 코드값과 docs/요구사항.md 표에 적힌 값이 같은지 비교해줘
```

### 기억할 4가지

| | |
|---|---|
| **한 번에 하나만** | 질문 하나에 물음표 하나 |
| **파일을 지정** | "어딘가에" 대신 "이 파일에서" |
| **먼저 찾고 나중에 읽기** | 검색으로 후보를 좁힌 뒤 그 파일만 읽게 한다 |
| **답을 검증** | AI가 알려준 파일·줄 번호를 직접 열어 확인 |

---

## 폴더 구성

```
roombook/
├── frontend/      화면 (html · css · js)
│   ├── components/  └ modals/
│   └── pages/       └ admin/
├── backend/       서버 (js · py)
│   ├── routes/      └ middleware/
│   └── services/    └ batch/
├── database/      스키마 (sql)
│   ├── migrations/  └ rollback/
│   └── tuning/      ← SQL 튜닝 실습
├── docs/          문서 (md · txt)
│   └── 회의록/      └ 첨부/
└── config/        설정 (yaml · yml · sh · txt)
    └── deploy/      └ scripts/
```

파일 42개 · 폴더 22개 · 최대 5뎁스

## 탐색해볼 파일 이름 예시

| 파일 | 어디에 |
|---|---|
| `app.js` | `roombook/frontend/` |
| `calendar-widget.js` | `roombook/frontend/components/` |
| `confirm-dialog.js` · `error-toast.js` | `roombook/frontend/components/modals/` |
| `booking-form.html` | `roombook/frontend/pages/` |
| `usage-report.js` · `feature-flags.json` | `roombook/frontend/pages/admin/` |
| `reservation-router.js` | `roombook/backend/routes/` |
| `time-range-check.js` · `auth-guard.js` | `roombook/backend/routes/middleware/` |
| `booking-service.js` | `roombook/backend/services/` |
| `nightly-sync.py` · `archive-cleaner.py` | `roombook/backend/services/batch/` |
| `schema.sql` · `seed-data.sql` | `roombook/database/` |
| `002-add-index.sql` | `roombook/database/migrations/` |
| `undo-002.sql` | `roombook/database/migrations/rollback/` |
| `slow-reservation-query.sql` · `slow-usage-report.sql` | `roombook/database/tuning/` |
| `요구사항.md` · `API명세.md` | `roombook/docs/` |
| `2026-07-03_중간점검.md` | `roombook/docs/회의록/` |
| `결정사항_요약.txt` | `roombook/docs/회의록/첨부/` |
| `docker-compose.yml` | `roombook/config/deploy/` |
| `health-check.sh` | `roombook/config/deploy/scripts/` |

---

# 문제

★ 쉬움 · ★★ 보통 · ★★★ 어려움
막히면 각 문제의 **힌트 프롬프트**를 그대로 복사해서 넣어보세요.

### 1. API 주소 ★

프론트엔드가 호출하는 API 기본 주소가 코드에 그대로 박혀 있습니다.
어느 파일이고, 주소는 무엇인가요?

> 힌트 · `API_BASE 라는 문자열이 있는 파일을 찾아줘`

### 2. 문서와 코드가 다르다 — 예약 시간 ★★

한 번에 예약할 수 있는 **최대 시간**이 문서와 코드에서 다릅니다.
각각 몇 시간이고, 어느 파일에 적혀 있나요? (문서 쪽은 3곳입니다)

> 힌트 1 · `MAX_HOURS 가 있는 파일을 찾아서 값을 알려줘`
> 힌트 2 · `"3시간" 이라는 문자열이 들어간 파일을 전부 찾아줘`

### 3. 문서와 데이터가 다르다 — 회의실 개수 ★★

회의록에 적힌 회의실 개수와 실제 초기 데이터 건수가 다릅니다. 각각 몇 개인가요?

> 힌트 1 · `docs/회의록/2026-07-03_중간점검.md 에서 회의실 개수를 찾아줘`
> 힌트 2 · `database/seed-data.sql 에서 INSERT INTO rooms 가 몇 줄인지 세어줘`

### 4. 이름이 같은 함수가 두 개 ★★

똑같은 이름의 함수가 서로 다른 두 파일에 정의돼 있습니다.
함수 이름과 두 파일은? 동작은 어떻게 다른가요?

> 힌트 1 · `formatTimeSlot 함수가 정의된 파일을 전부 찾아줘`
> 힌트 2 · `두 파일의 formatTimeSlot 을 비교해서 출력 형식 차이를 설명해줘`

### 5. TODO 주석 ★

프로젝트에 `TODO:` 주석이 몇 개 있고, 각각 어느 파일에 있나요?

> 힌트 · `TODO: 로 시작하는 주석을 전부 찾아줘`
> (이 README 자체도 걸립니다. `roombook/` 안쪽만 세세요)

### 6. 예약 겹침 버그 ★★★

`booking-service.js` 의 `hasConflict()` 함수에 **경계 조건 버그**가 있습니다.
어느 줄이고, 무엇이 잘못됐나요?

> 힌트 1 · `backend/services/booking-service.js 의 hasConflict 함수만 보여줘`
> 힌트 2 · `새 예약의 끝시각이 기존 예약의 시작시각과 정확히 같을 때 이 함수가 어떻게 판정하는지 설명해줘`
> 힌트 3 · 부등호 두 개를 나란히 비교해보세요. 한쪽만 이상합니다.

### 7. 노출된 비밀번호 ★

설정 파일 한 곳에 DB 비밀번호가 그대로 적혀 있습니다. 어느 파일인가요?
(연습용 가짜 값입니다)

> 힌트 · `config 폴더에서 비밀번호가 하드코딩된 파일을 찾아줘`

### 8. 인덱스 없는 테이블 ★★★

테이블 4개 중 인덱스가 한 번도 만들어지지 않은 테이블이 하나 있습니다. 어느 테이블인가요?

> 힌트 1 · `database/schema.sql 에서 CREATE TABLE 이름을 전부 뽑아줘`
> 힌트 2 · `database 폴더 전체에서 CREATE INDEX 가 있는 줄을 찾아줘`
> 힌트 3 · 두 목록을 직접 대조해보세요. 한 번에 시키면 틀리기 쉽습니다.

---

## 보너스

- 5뎁스(가장 깊은 곳)에 있는 파일 3개의 이름은?
  > `undo-002.sql 파일의 전체 경로를 알려줘`
- `deprecated-notice.md` 가 말하는 제거 예정일은?
- **아무도 호출하지 않는 함수**를 하나 찾아보세요. ★★★
  > `error-toast.js 에 정의된 함수 이름을 알려줘`
  > → `그 함수 이름을 프로젝트 전체에서 검색해줘`

---

# 추가 과제 — SQL 튜닝 (2문제)

탐색 문제를 다 풀었으면 이쪽으로 넘어오세요.
**찾는 연습이 아니라 고치는 연습**입니다.

파일 2개에 문제 상황·현재 인덱스·실행계획이 주석으로 다 적혀 있습니다.
`.sql` 이라 VS Code에서 그냥 열리고 색도 입혀집니다.

| 파일 | 내용 | 난이도 |
|---|---|---|
| `database/tuning/slow-reservation-query.sql` | 인덱스를 못 쓰는 조회 쿼리 (원인 4개+) | ★★ |
| `database/tuning/slow-usage-report.sql` | 서브쿼리 3개 반복 스캔 + 인덱스 누락 | ★★★ |

### 이렇게 물어보세요

한 번에 "최적화해줘"라고 하면 35B 모델은 엉뚱한 걸 고칩니다.
**한 가지씩** 물어야 정확합니다.

```
database/tuning/slow-reservation-query.sql 파일을 읽고,
주석에 적힌 인덱스 목록과 쿼리의 WHERE 조건을 비교해줘
```

```
이 쿼리에서 start_at 컬럼에 DATE() 함수를 쓰면
idx_reservations_room_time 인덱스를 탈 수 있는지 설명해줘
```

```
emp_no 컬럼 타입이 VARCHAR(7) 인데 = 1234567 로 비교하고 있어.
무슨 문제가 생기는지 알려줘
```

```
위에서 찾은 문제들을 반영해서 쿼리를 다시 써줘.
필요한 컬럼은 파일 주석의 "화면에서 실제로 필요한 컬럼" 목록만 쓰고
```

### 반드시 확인할 것

AI가 고쳐준 쿼리를 **그대로 믿지 마세요.** 이 두 가지를 직접 따져보세요.

1. **결과가 같은가** — 조건을 바꾸면서 결과 집합이 달라지지 않았는지
   (특히 B-1에서 예약 0건인 회의실이 사라지지 않았는지)
2. **인덱스를 실제로 타는가** — 왜 빨라지는지 한 줄로 설명할 수 있는지

35B 모델은 `DATE(start_at) = '...'` 를 `start_at >= '...' AND start_at < '...'`
로 바꾸는 것까지는 잘 하지만, **경계값을 틀리게 잡는 경우가 있습니다.**
`<=` 인지 `<` 인지 직접 확인하세요.

---

## 마치고 나서

`_강사용/정답지.md` 로 채점하세요.
정답보다 **어떤 질문을 던져서 찾았는지**가 더 중요합니다.
잘 통했던 질문 한 문장을 기억해 가세요.
