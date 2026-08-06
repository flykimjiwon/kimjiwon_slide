#!/usr/bin/env python3
"""SBTI 실습 과제 트리 생성 — 회의실 예약 시스템(가상 프로젝트) 탐색 과제.

최대 5뎁스, 모든 폴더에 파일, 파일명 전부 고유, html/js/md/sql/py/json/yaml/txt/css/sh 혼합.
정답의 근거가 실제 파일 내용에 심겨 있다.
"""
import os, io, textwrap, zipfile

ROOT = '/Users/kimjiwon/Desktop/SBTI_PDF_모음_2026-08-05/06_실습과제'

F = {}   # 상대경로 -> 내용

# ─────────────────────────────── 1뎁스
F['README.md'] = '''# SBTI 실습 — 코드베이스 탐색 과제

처음 보는 프로젝트를 **택가이 코드어시스턴트로 파악하는** 연습입니다.
가상의 사내 시스템 `roombook`(회의실 예약)이 들어 있습니다. 직접 열어보지 말고,
**AI에게 물어서** 답을 찾아보세요.

## 이렇게 시작하세요

```
cd roombook
techai
```

그리고 이렇게 물어보세요.

```
이 프로젝트 구조를 요약해줘
예약 시간 제한이 어디서 정해지는지 찾아줘
문서랑 코드가 서로 다른 부분이 있는지 확인해줘
```

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
│   └── migrations/  └ rollback/
├── docs/          문서 (md · txt)
│   └── 회의록/      └ 첨부/
└── config/        설정 (yaml · yml · sh · txt)
    └── deploy/      └ scripts/
```

## 탐색해볼 파일 이름 예시

| 파일 | 어디에 |
|---|---|
| `app.js` | `roombook/frontend/` |
| `calendar-widget.js` | `roombook/frontend/components/` |
| `confirm-dialog.js` | `roombook/frontend/components/modals/` |
| `booking-form.html` | `roombook/frontend/pages/` |
| `usage-report.js` | `roombook/frontend/pages/admin/` |
| `reservation-router.js` | `roombook/backend/routes/` |
| `time-range-check.js` | `roombook/backend/routes/middleware/` |
| `booking-service.js` | `roombook/backend/services/` |
| `nightly-sync.py` | `roombook/backend/services/batch/` |
| `schema.sql` | `roombook/database/` |
| `002-add-index.sql` | `roombook/database/migrations/` |
| `undo-002.sql` | `roombook/database/migrations/rollback/` |
| `요구사항.md` | `roombook/docs/` |
| `2026-07-03_중간점검.md` | `roombook/docs/회의록/` |
| `결정사항_요약.txt` | `roombook/docs/회의록/첨부/` |
| `docker-compose.yml` | `roombook/config/deploy/` |
| `health-check.sh` | `roombook/config/deploy/scripts/` |

---

# 문제 (8개)

풀고 나서 `_강사용/정답지.md` 로 채점하세요.

**1. API 주소**
프론트엔드가 호출하는 API 기본 주소가 코드에 그대로 박혀 있습니다.
어느 파일이고, 주소는 무엇인가요?

**2. 문서와 코드의 불일치 — 예약 시간**
한 번에 예약할 수 있는 최대 시간이 **문서와 코드에서 다릅니다.**
각각 몇 시간이고, 어느 파일에 적혀 있나요?

**3. 문서와 데이터의 불일치 — 회의실 개수**
회의록에 적힌 회의실 개수와 실제 초기 데이터의 개수가 다릅니다.
각각 몇 개인가요?

**4. 중복 함수**
이름이 똑같은 함수가 서로 다른 두 파일에 각각 정의돼 있습니다.
함수 이름과 두 파일은 무엇인가요? 동작도 미묘하게 다른데, 어떻게 다른가요?

**5. TODO 주석**
프로젝트 전체에 `TODO:` 주석이 몇 개 있고, 각각 어느 파일에 있나요?

**6. 예약 겹침 버그**
예약이 겹치는지 검사하는 로직에 경계 조건 버그가 있습니다.
어느 파일 몇 번째 줄이고, 무엇이 잘못됐나요?

**7. 노출된 비밀번호**
설정 파일 한 곳에 DB 비밀번호가 그대로 적혀 있습니다. 어느 파일인가요?
(연습용 가짜 값입니다)

**8. 인덱스 없는 테이블**
테이블 4개 중 인덱스가 한 번도 만들어지지 않은 테이블이 하나 있습니다.
어느 테이블인가요?

---

## 보너스

- 가장 깊은 곳(5뎁스)에 있는 파일 3개의 이름은?
- `deprecated-notice.md` 가 말하는 제거 예정일은 언제인가요?
- 이 프로젝트에서 **아무도 호출하지 않는 함수**를 하나 찾아보세요.
'''

F['_강사용/정답지.md'] = '''# 정답지 (강사용)

> 배포 전에 이 폴더(`_강사용/`)를 지우고 주세요.

**1. API 주소**
`roombook/frontend/app.js` 3번째 줄
`https://roombook.internal.example/api/v2`

**2. 예약 최대 시간 — 문서 3시간 / 코드 4시간**
- 문서: `roombook/docs/요구사항.md` — "1회 예약은 최대 **3시간**"
- 코드: `roombook/backend/routes/middleware/time-range-check.js` — `const MAX_HOURS = 4;`
- `roombook/docs/API명세.md` 에도 3시간으로 적혀 있어 문서 2곳 vs 코드 1곳.

**3. 회의실 개수 — 회의록 8개 / 데이터 7개**
- `roombook/docs/회의록/2026-07-03_중간점검.md` — "회의실 8개 전부 등록 완료"
- `roombook/database/seed-data.sql` — INSERT 7건 (R-101 ~ R-107)

**4. 중복 함수 `formatTimeSlot`**
- `roombook/frontend/components/calendar-widget.js` — 24시간제 (`14:00`)
- `roombook/frontend/pages/admin/usage-report.js` — 12시간제 (`2:00 PM`)
- 같은 이름인데 출력 형식이 달라, 화면에 따라 시간 표기가 달라진다.

**5. TODO 주석 3개**
- `roombook/backend/services/booking-service.js`
- `roombook/frontend/pages/admin/usage-report.js`
- `roombook/backend/services/batch/nightly-sync.py`

**6. 예약 겹침 버그**
`roombook/backend/services/booking-service.js` 의 `hasConflict()`

```js
if (newStart >= r.end_at || newEnd < r.start_at) continue;   // ← 버그
```

뒤쪽이 `<` 라서 **새 예약의 끝 시각과 기존 예약의 시작 시각이 같을 때**(딱 붙는 예약)
겹친다고 잘못 판단한다. `<=` 여야 한다.
앞쪽(`>=`)은 올바르므로 한쪽만 틀린 비대칭 버그다.

**7. 노출된 비밀번호**
`roombook/config/deploy/docker-compose.yml`
`ROOMBOOK_DB_PASS=P@ssw0rd!2026` (연습용 가짜)
`config/env.example.txt` 는 placeholder 라 정상.

**8. 인덱스 없는 테이블 — `audit_log`**
- `schema.sql`: rooms(PK+idx), users(PK+idx), reservations(PK)
- `migrations/002-add-index.sql`: reservations 에 인덱스 추가
- `audit_log` 는 어디에서도 인덱스가 없다.
- 함정: `rollback/undo-002.sql` 은 reservations 인덱스를 지우지만 실행 전제가 아니다.

---

## 보너스 정답

**5뎁스 파일** — `undo-002.sql`, `health-check.sh`, `결정사항_요약.txt`,
그리고 `modals/`·`admin/`·`middleware/`·`batch/` 안의 파일들

**제거 예정일** — 2026-09-30 (`frontend/components/modals/deprecated-notice.md`)

**아무도 호출하지 않는 함수** — `roombook/frontend/components/modals/error-toast.js` 의
`showLegacyToast()`. 프로젝트 어디에서도 참조되지 않는다.
'''

# ─────────────────────────────── roombook 루트
F['roombook/PROJECT.md'] = '''# roombook — 사내 회의실 예약 시스템 (연습용 가상 프로젝트)

실제 운영 시스템이 아니라 **교육 실습용으로 만든 가짜 코드베이스**입니다.

- 프론트: 순수 HTML/CSS/JS
- 백엔드: Node.js (Express 스타일)
- 배치: Python
- DB: PostgreSQL

## 실행 (실습에서는 실행하지 않습니다)

```
npm install
npm run dev
```

## 담당

| 영역 | 담당 |
|---|---|
| 화면 | 프론트 파트 |
| 서버·배치 | 백엔드 파트 |
| DB | 데이터 파트 |
'''

F['roombook/package.json'] = '''{
  "name": "roombook",
  "version": "0.4.2",
  "private": true,
  "description": "사내 회의실 예약 시스템 (교육 실습용 가상 프로젝트)",
  "scripts": {
    "dev": "node backend/server.js",
    "batch:sync": "python3 backend/services/batch/nightly-sync.py",
    "db:migrate": "psql -f database/migrations/001-create-rooms.sql"
  },
  "dependencies": {
    "express": "^4.19.2",
    "pg": "^8.11.5"
  }
}
'''

# ─────────────────────────────── frontend
F['roombook/frontend/index.html'] = '''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>roombook — 회의실 예약</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="topbar">
    <h1>회의실 예약</h1>
    <nav>
      <a href="pages/booking-form.html">새 예약</a>
      <a href="pages/my-reservations.html">내 예약</a>
      <a href="pages/admin/dashboard-panel.html">관리자</a>
    </nav>
  </header>

  <main id="app">
    <div id="calendar-root"></div>
  </main>

  <script src="components/calendar-widget.js"></script>
  <script src="components/modals/confirm-dialog.js"></script>
  <script src="app.js"></script>
</body>
</html>
'''

F['roombook/frontend/style.css'] = '''/* roombook 기본 스타일 */
:root {
  --brand: #0066cc;
  --line: #e2e7ee;
  --text: #1a1a1a;
  --muted: #5f6672;
}

body { margin: 0; font-family: system-ui, sans-serif; color: var(--text); }

.topbar {
  display: flex; align-items: center; gap: 24px;
  padding: 14px 24px; border-bottom: 1px solid var(--line);
}
.topbar h1 { font-size: 18px; margin: 0; }
.topbar nav a { margin-right: 14px; color: var(--brand); text-decoration: none; }

.room-card { border: 1px solid var(--line); border-radius: 12px; padding: 16px; }
.room-card.full { opacity: .5; }

.slot { display: inline-block; padding: 6px 10px; border-radius: 999px; }
.slot.free { background: #eff6ff; color: var(--brand); }
.slot.taken { background: #f1f5f9; color: var(--muted); }
'''

F['roombook/frontend/app.js'] = '''// roombook 프론트엔드 진입점

const API_BASE = 'https://roombook.internal.example/api/v2';

const state = {
  rooms: [],
  selectedDate: new Date().toISOString().slice(0, 10),
};

async function loadRooms() {
  const res = await fetch(`${API_BASE}/rooms`);
  state.rooms = await res.json();
  renderCalendar(state.rooms, state.selectedDate);
}

async function submitReservation(payload) {
  const res = await fetch(`${API_BASE}/reservations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    showConfirmDialog('예약에 실패했습니다', await res.text());
    return null;
  }
  return res.json();
}

document.addEventListener('DOMContentLoaded', loadRooms);
'''

F['roombook/frontend/components/calendar-widget.js'] = '''// 달력 위젯 — 날짜별 회의실 가용 슬롯을 그린다

const SLOT_MINUTES = 30;

function formatTimeSlot(hour, minute) {
  // 24시간제로 표기한다  (예: 14:00)
  const h = String(hour).padStart(2, '0');
  const m = String(minute).padStart(2, '0');
  return `${h}:${m}`;
}

function buildSlots(openHour, closeHour) {
  const slots = [];
  for (let h = openHour; h < closeHour; h++) {
    for (let m = 0; m < 60; m += SLOT_MINUTES) {
      slots.push(formatTimeSlot(h, m));
    }
  }
  return slots;
}

function renderCalendar(rooms, dateStr) {
  const root = document.getElementById('calendar-root');
  if (!root) return;
  root.innerHTML = rooms
    .map((r) => `<div class="room-card"><b>${r.name}</b><span>${dateStr}</span></div>`)
    .join('');
}
'''

F['roombook/frontend/components/room-card.html'] = '''<!-- 회의실 카드 조각 — app.js 가 문자열로 조립해 쓴다 -->
<div class="room-card" data-room-id="{{ROOM_ID}}">
  <b class="room-name">{{ROOM_NAME}}</b>
  <p class="room-meta">{{FLOOR}}층 · 정원 {{CAPACITY}}명</p>
  <div class="room-slots">
    <span class="slot free">{{SLOT_1}}</span>
    <span class="slot taken">{{SLOT_2}}</span>
  </div>
  <button class="btn-book" data-action="book">예약</button>
</div>
'''

F['roombook/frontend/components/modals/confirm-dialog.js'] = '''// 확인 다이얼로그

function showConfirmDialog(title, message) {
  const box = document.createElement('div');
  box.className = 'dialog';
  box.innerHTML = `<h3>${title}</h3><p>${message}</p><button>확인</button>`;
  box.querySelector('button').addEventListener('click', () => box.remove());
  document.body.appendChild(box);
  return box;
}
'''

F['roombook/frontend/components/modals/error-toast.js'] = '''// 오류 토스트

function showErrorToast(message, ms = 3000) {
  const el = document.createElement('div');
  el.className = 'toast toast-error';
  el.textContent = message;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), ms);
}

// 구버전 호환용으로 남겨둔 함수 — 현재 아무 데서도 호출하지 않는다
function showLegacyToast(message) {
  window.alert('[roombook] ' + message);
}
'''

F['roombook/frontend/components/modals/deprecated-notice.md'] = '''# modals 폴더 정리 안내

`showLegacyToast()` 는 2025년 구버전 화면에서만 쓰던 함수입니다.
현재는 `showErrorToast()` 로 모두 교체됐습니다.

- **제거 예정일: 2026-09-30**
- 그때까지 남겨두는 이유: 사외 협력사 화면 한 곳에서 참조 여부 확인 중

제거할 때 `error-toast.js` 안의 해당 함수만 지우면 됩니다.
'''

F['roombook/frontend/pages/booking-form.html'] = '''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>새 예약 — roombook</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <h2>새 예약</h2>

  <form id="booking-form">
    <label>회의실
      <select name="roomId" required></select>
    </label>
    <label>날짜
      <input type="date" name="date" required>
    </label>
    <label>시작
      <input type="time" name="startAt" required>
    </label>
    <label>종료
      <input type="time" name="endAt" required>
    </label>
    <label>목적
      <input type="text" name="purpose" maxlength="60">
    </label>

    <p class="hint">1회 예약은 최대 3시간까지 가능합니다.</p>
    <button type="submit">예약하기</button>
  </form>

  <script src="../app.js"></script>
</body>
</html>
'''

F['roombook/frontend/pages/my-reservations.html'] = '''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>내 예약 — roombook</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <h2>내 예약</h2>

  <table id="my-reservation-table">
    <thead>
      <tr><th>날짜</th><th>회의실</th><th>시간</th><th>상태</th><th></th></tr>
    </thead>
    <tbody><!-- app.js 가 채운다 --></tbody>
  </table>

  <p class="hint">지난 예약은 30일까지만 보관됩니다.</p>
  <script src="../app.js"></script>
</body>
</html>
'''

F['roombook/frontend/pages/admin/dashboard-panel.html'] = '''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>관리자 — roombook</title>
  <link rel="stylesheet" href="../../style.css">
</head>
<body>
  <h2>관리자 대시보드</h2>

  <section class="stat-row">
    <div><b id="stat-total">-</b><span>전체 예약</span></div>
    <div><b id="stat-today">-</b><span>오늘 예약</span></div>
    <div><b id="stat-rooms">-</b><span>회의실</span></div>
  </section>

  <section>
    <h3>회의실별 이용률</h3>
    <div id="usage-chart"></div>
  </section>

  <script src="usage-report.js"></script>
</body>
</html>
'''

F['roombook/frontend/pages/admin/usage-report.js'] = '''// 관리자 — 회의실 이용률 리포트

function formatTimeSlot(hour, minute) {
  // 관리자 화면은 12시간제로 표기한다  (예: 2:00 PM)
  const suffix = hour >= 12 ? 'PM' : 'AM';
  const h12 = hour % 12 === 0 ? 12 : hour % 12;
  const m = String(minute).padStart(2, '0');
  return `${h12}:${m} ${suffix}`;
}

function calcUsageRate(reservedMinutes, openMinutes) {
  if (openMinutes <= 0) return 0;
  return Math.round((reservedMinutes / openMinutes) * 100);
}

// TODO: 부서별 집계도 추가해야 함 (2026-07-03 중간점검에서 요청)
function renderUsageChart(rows) {
  const root = document.getElementById('usage-chart');
  if (!root) return;
  root.innerHTML = rows
    .map((r) => `<div>${r.roomName} — ${calcUsageRate(r.used, r.open)}%</div>`)
    .join('');
}
'''

F['roombook/frontend/pages/admin/feature-flags.json'] = '''{
  "_comment": "관리자 화면 기능 토글. 실습용 가짜 설정",
  "flags": {
    "showDepartmentBreakdown": false,
    "allowBulkCancel": true,
    "enableNewCalendar": false,
    "exportToExcel": true,
    "showLegacyToast": false
  },
  "updatedAt": "2026-07-15",
  "owner": "backend-team"
}
'''

# ─────────────────────────────── backend
F['roombook/backend/server.js'] = '''// roombook 백엔드 진입점

const express = require('express');
const reservationRouter = require('./routes/reservation-router');
const roomRouter = require('./routes/room-router');
const authGuard = require('./routes/middleware/auth-guard');
const rateLimiter = require('./routes/middleware/rate-limiter');

const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.json());
app.use(rateLimiter);
app.use('/api/v2', authGuard);
app.use('/api/v2/reservations', reservationRouter);
app.use('/api/v2/rooms', roomRouter);

app.get('/healthz', (req, res) => res.json({ ok: true, version: '0.4.2' }));

app.listen(PORT, () => console.log(`roombook api on :${PORT}`));
'''

F['roombook/backend/routes/reservation-router.js'] = '''// 예약 라우터

const express = require('express');
const bookingService = require('../services/booking-service');
const checkTimeRange = require('./middleware/time-range-check');

const router = express.Router();

router.get('/', async (req, res) => {
  const rows = await bookingService.listByUser(req.user.id);
  res.json(rows);
});

router.post('/', checkTimeRange, async (req, res) => {
  const result = await bookingService.create(req.user.id, req.body);
  if (result.error) return res.status(409).json({ message: result.error });
  res.status(201).json(result.reservation);
});

router.delete('/:id', async (req, res) => {
  await bookingService.cancel(req.user.id, req.params.id);
  res.status(204).end();
});

module.exports = router;
'''

F['roombook/backend/routes/room-router.js'] = '''// 회의실 라우터

const express = require('express');
const router = express.Router();

const OPEN_HOUR = 8;
const CLOSE_HOUR = 20;

router.get('/', async (req, res) => {
  const rooms = await req.db.query('SELECT * FROM rooms WHERE active = true ORDER BY code');
  res.json({ openHour: OPEN_HOUR, closeHour: CLOSE_HOUR, rooms: rooms.rows });
});

router.get('/:code', async (req, res) => {
  const one = await req.db.query('SELECT * FROM rooms WHERE code = $1', [req.params.code]);
  if (one.rowCount === 0) return res.status(404).json({ message: '없는 회의실' });
  res.json(one.rows[0]);
});

module.exports = router;
'''

F['roombook/backend/routes/middleware/auth-guard.js'] = '''// 사번 기반 인증 확인

module.exports = function authGuard(req, res, next) {
  const empNo = req.header('X-Emp-No');
  if (!empNo) {
    return res.status(401).json({ message: '사번 헤더가 없습니다' });
  }
  if (!/^[0-9]{7}$/.test(empNo)) {
    return res.status(400).json({ message: '사번 형식이 올바르지 않습니다' });
  }
  req.user = { id: empNo };
  next();
};
'''

F['roombook/backend/routes/middleware/rate-limiter.js'] = '''// 아주 단순한 요청 제한기 (메모리 기반)

const WINDOW_MS = 60 * 1000;
const MAX_REQUESTS = 60;

const hits = new Map();

module.exports = function rateLimiter(req, res, next) {
  const key = req.header('X-Emp-No') || req.ip;
  const now = Date.now();
  const bucket = hits.get(key) || { count: 0, resetAt: now + WINDOW_MS };

  if (now > bucket.resetAt) {
    bucket.count = 0;
    bucket.resetAt = now + WINDOW_MS;
  }
  bucket.count += 1;
  hits.set(key, bucket);

  if (bucket.count > MAX_REQUESTS) {
    return res.status(429).json({ message: '요청이 너무 많습니다' });
  }
  next();
};
'''

F['roombook/backend/routes/middleware/time-range-check.js'] = '''// 예약 시간 범위 검증

const MAX_HOURS = 4;
const MIN_MINUTES = 30;

module.exports = function checkTimeRange(req, res, next) {
  const { startAt, endAt } = req.body;
  const start = new Date(startAt);
  const end = new Date(endAt);

  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    return res.status(400).json({ message: '시간 형식이 올바르지 않습니다' });
  }
  if (end <= start) {
    return res.status(400).json({ message: '종료 시각이 시작보다 빠릅니다' });
  }

  const minutes = (end - start) / 60000;
  if (minutes < MIN_MINUTES) {
    return res.status(400).json({ message: `최소 ${MIN_MINUTES}분 이상이어야 합니다` });
  }
  if (minutes > MAX_HOURS * 60) {
    return res.status(400).json({ message: `1회 예약은 최대 ${MAX_HOURS}시간입니다` });
  }
  next();
};
'''

F['roombook/backend/routes/middleware/payload-schema.json'] = '''{
  "_comment": "예약 생성 요청 본문 스키마 (실습용)",
  "type": "object",
  "required": ["roomId", "startAt", "endAt"],
  "properties": {
    "roomId":  { "type": "string", "pattern": "^R-[0-9]{3}$" },
    "startAt": { "type": "string", "format": "date-time" },
    "endAt":   { "type": "string", "format": "date-time" },
    "purpose": { "type": "string", "maxLength": 60 },
    "attendees": { "type": "integer", "minimum": 1, "maximum": 30 }
  },
  "additionalProperties": false
}
'''

F['roombook/backend/services/booking-service.js'] = '''// 예약 서비스 — 겹침 검사와 저장

async function listByUser(userId) {
  return db.query(
    'SELECT * FROM reservations WHERE emp_no = $1 ORDER BY start_at DESC',
    [userId]
  );
}

/**
 * 새 예약이 기존 예약과 겹치는지 검사한다.
 * 겹치면 true.
 */
function hasConflict(existing, newStart, newEnd) {
  for (const r of existing) {
    // 완전히 앞이거나 완전히 뒤면 겹치지 않는다
    if (newStart >= r.end_at || newEnd < r.start_at) continue;
    return true;
  }
  return false;
}

async function create(userId, payload) {
  const rows = await db.query(
    'SELECT start_at, end_at FROM reservations WHERE room_id = $1 AND status = $2',
    [payload.roomId, 'CONFIRMED']
  );

  if (hasConflict(rows, new Date(payload.startAt), new Date(payload.endAt))) {
    return { error: '이미 예약된 시간입니다' };
  }

  // TODO: 예약 확정 메일 발송을 notify-service 로 옮기기
  const saved = await db.query(
    'INSERT INTO reservations (room_id, emp_no, start_at, end_at, purpose, status) VALUES ($1,$2,$3,$4,$5,$6) RETURNING *',
    [payload.roomId, userId, payload.startAt, payload.endAt, payload.purpose, 'CONFIRMED']
  );
  return { reservation: saved.rows[0] };
}

async function cancel(userId, reservationId) {
  return db.query(
    'UPDATE reservations SET status = $1 WHERE id = $2 AND emp_no = $3',
    ['CANCELLED', reservationId, userId]
  );
}

module.exports = { listByUser, create, cancel, hasConflict };
'''

F['roombook/backend/services/notify-service.js'] = '''// 알림 서비스 — 사내 메일/메신저 발송 (실습용 스텁)

const TEMPLATES = {
  CONFIRMED: '[roombook] 예약이 확정되었습니다',
  CANCELLED: '[roombook] 예약이 취소되었습니다',
  REMINDER: '[roombook] 30분 뒤 회의가 시작됩니다',
};

async function sendMail(empNo, templateKey, vars) {
  const subject = TEMPLATES[templateKey];
  if (!subject) throw new Error('알 수 없는 템플릿: ' + templateKey);
  console.log(`[mail] to=${empNo} subject=${subject}`, vars);
  return { ok: true };
}

async function sendReminderBatch(reservations) {
  const results = [];
  for (const r of reservations) {
    results.push(await sendMail(r.emp_no, 'REMINDER', { room: r.room_id }));
  }
  return results;
}

module.exports = { sendMail, sendReminderBatch, TEMPLATES };
'''

F['roombook/backend/services/batch/nightly-sync.py'] = '''#!/usr/bin/env python3
"""야간 동기화 배치 — 인사 시스템에서 사번/부서를 받아 users 테이블을 갱신한다."""

import datetime

BATCH_NAME = "nightly-sync"
SOURCE_SYSTEM = "HR-MASTER"
CHUNK_SIZE = 500


def fetch_employees(cursor_date):
    """인사 시스템에서 변경분을 가져온다 (실습용 더미)."""
    return [
        {"emp_no": "1234567", "name": "홍길동", "dept": "디지털서비스개발부"},
        {"emp_no": "2345678", "name": "김철수", "dept": "정보서비스개발부"},
    ]


def upsert_users(rows):
    for row in rows:
        print(f"upsert {row['emp_no']} {row['dept']}")
    return len(rows)


# TODO: 실패한 청크만 재시도하는 로직 추가
def main():
    started = datetime.datetime.now()
    rows = fetch_employees(started.date())
    count = upsert_users(rows)
    print(f"[{BATCH_NAME}] {count}건 처리 · 소스={SOURCE_SYSTEM}")


if __name__ == "__main__":
    main()
'''

F['roombook/backend/services/batch/archive-cleaner.py'] = '''#!/usr/bin/env python3
"""보관 기간이 지난 예약을 정리한다."""

RETENTION_DAYS = 30
TARGET_TABLE = "reservations"


def find_expired(conn, retention_days=RETENTION_DAYS):
    sql = (
        f"SELECT id FROM {TARGET_TABLE} "
        "WHERE status = 'CANCELLED' AND end_at < NOW() - INTERVAL '%s days'"
    )
    return conn.execute(sql, (retention_days,)).fetchall()


def archive(conn, ids):
    if not ids:
        print("정리 대상 없음")
        return 0
    conn.execute("INSERT INTO audit_log (action, target_id) VALUES ('ARCHIVE', %s)", ids)
    return len(ids)


if __name__ == "__main__":
    print(f"보관 기간 {RETENTION_DAYS}일 기준으로 정리합니다")
'''

# ─────────────────────────────── database
F['roombook/database/schema.sql'] = '''-- roombook 스키마 (실습용)

CREATE TABLE rooms (
  id        SERIAL PRIMARY KEY,
  code      VARCHAR(10) NOT NULL UNIQUE,
  name      VARCHAR(60) NOT NULL,
  floor     SMALLINT    NOT NULL,
  capacity  SMALLINT    NOT NULL,
  active    BOOLEAN     NOT NULL DEFAULT TRUE
);
CREATE INDEX idx_rooms_floor ON rooms (floor);

CREATE TABLE users (
  emp_no    VARCHAR(7) PRIMARY KEY,
  name      VARCHAR(30) NOT NULL,
  dept      VARCHAR(60) NOT NULL,
  joined_at DATE
);
CREATE INDEX idx_users_dept ON users (dept);

CREATE TABLE reservations (
  id        SERIAL PRIMARY KEY,
  room_id   VARCHAR(10) NOT NULL,
  emp_no    VARCHAR(7)  NOT NULL,
  start_at  TIMESTAMP   NOT NULL,
  end_at    TIMESTAMP   NOT NULL,
  purpose   VARCHAR(60),
  status    VARCHAR(12) NOT NULL DEFAULT 'CONFIRMED'
);
-- 인덱스는 002-add-index.sql 에서 추가한다

CREATE TABLE audit_log (
  id         SERIAL PRIMARY KEY,
  action     VARCHAR(20) NOT NULL,
  target_id  INTEGER,
  actor      VARCHAR(7),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
'''

F['roombook/database/seed-data.sql'] = '''-- 초기 회의실 데이터

INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-101', '집중회의실 A',  10,  4);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-102', '집중회의실 B',  10,  4);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-103', '중회의실 1',    10, 10);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-104', '중회의실 2',    11, 10);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-105', '대회의실',      11, 24);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-106', '화상회의실',    12,  8);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-107', '교육장',        12, 40);

INSERT INTO users (emp_no, name, dept, joined_at) VALUES ('1234567', '홍길동', '디지털서비스개발부', '2019-03-04');
INSERT INTO users (emp_no, name, dept, joined_at) VALUES ('2345678', '김철수', '정보서비스개발부',   '2021-09-01');
'''

F['roombook/database/migrations/001-create-rooms.sql'] = '''-- 001 : 회의실 테이블 생성
-- 적용일 2026-06-14

BEGIN;

CREATE TABLE IF NOT EXISTS rooms (
  id       SERIAL PRIMARY KEY,
  code     VARCHAR(10) NOT NULL UNIQUE,
  name     VARCHAR(60) NOT NULL,
  floor    SMALLINT    NOT NULL,
  capacity SMALLINT    NOT NULL,
  active   BOOLEAN     NOT NULL DEFAULT TRUE
);

COMMIT;
'''

F['roombook/database/migrations/002-add-index.sql'] = '''-- 002 : 예약 조회 성능 개선
-- 적용일 2026-07-02
-- 배경: 내 예약 목록 조회가 느리다는 접수 (2026-07-03 중간점검 참고)

BEGIN;

CREATE INDEX idx_reservations_room_time ON reservations (room_id, start_at, end_at);
CREATE INDEX idx_reservations_emp ON reservations (emp_no);

COMMIT;
'''

F['roombook/database/migrations/rollback/undo-002.sql'] = '''-- 002 되돌리기
-- 인덱스 생성이 운영 중 잠금을 유발할 때만 실행한다. 평상시에는 실행하지 않는다.

BEGIN;

DROP INDEX IF EXISTS idx_reservations_room_time;
DROP INDEX IF EXISTS idx_reservations_emp;

COMMIT;
'''

# ─────────────────────────────── docs
F['roombook/docs/요구사항.md'] = '''# roombook 요구사항 (v0.4)

## 예약 규칙

| 항목 | 값 |
|---|---|
| 운영 시간 | 08:00 ~ 20:00 |
| 최소 예약 단위 | 30분 |
| **1회 예약 최대 시간** | **3시간** |
| 동시 보유 가능 예약 | 5건 |
| 취소 가능 시점 | 시작 30분 전까지 |

## 사용자

- 사번 7자리로 식별한다.
- 부서 정보는 인사 시스템에서 야간 배치로 받아온다.

## 화면

1. 달력에서 회의실별 빈 슬롯을 본다
2. 예약 폼에서 시간과 목적을 입력한다
3. 내 예약에서 취소한다
4. 관리자는 이용률을 본다
'''

F['roombook/docs/API명세.md'] = '''# roombook API 명세 (v2)

Base: `/api/v2`
인증: `X-Emp-No` 헤더 (사번 7자리)

## GET /rooms

```json
{ "openHour": 8, "closeHour": 20, "rooms": [ { "code": "R-101", "name": "집중회의실 A" } ] }
```

## POST /reservations

요청

```json
{ "roomId": "R-101", "startAt": "2026-08-10T14:00:00", "endAt": "2026-08-10T16:00:00", "purpose": "주간회의" }
```

제약

- `endAt` 은 `startAt` 보다 뒤여야 한다
- 최소 30분, **최대 3시간**
- 같은 회의실에 겹치는 예약이 있으면 `409`

응답 `201`

```json
{ "id": 1024, "status": "CONFIRMED" }
```

## DELETE /reservations/:id

응답 `204`
'''

F['roombook/docs/회의록/2026-06-12_킥오프.md'] = '''# roombook 킥오프 회의록

- 일시: 2026-06-12 14:00 ~ 15:00
- 장소: 중회의실 1
- 참석: 프론트 파트, 백엔드 파트, 데이터 파트

## 결정

1. 사번 기반 인증으로 간다. 별도 로그인 화면은 만들지 않는다.
2. 1차 범위는 예약 생성/조회/취소까지. 반복 예약은 2차로 미룬다.
3. 회의실 정보는 총무팀 엑셀을 받아 초기 적재한다.

## 남은 일

- 회의실 목록 최종본 수령 (총무팀)
- 예약 최대 시간 정책 확정 → 요구사항 문서에 반영
'''

F['roombook/docs/회의록/2026-07-03_중간점검.md'] = '''# roombook 중간점검 회의록

- 일시: 2026-07-03 10:00 ~ 11:00
- 참석: 전체

## 진행 상황

- 예약 생성/조회/취소 개발 완료
- **회의실 8개 전부 등록 완료** (총무팀 목록 반영)
- 관리자 이용률 화면 초안 완성

## 접수된 이슈

1. 내 예약 목록 조회가 느리다 → 인덱스 추가하기로 (002 마이그레이션)
2. 관리자 화면에 **부서별 집계**도 보고 싶다 → 다음 스프린트
3. 화면마다 시간 표기가 다르게 보인다는 제보 → 확인 필요

## 다음 점검

- 2026-07-24
'''

F['roombook/docs/회의록/첨부/결정사항_요약.txt'] = '''roombook 결정사항 요약 (2026-07-03 기준)

[확정]
- 인증: 사번 7자리 헤더 방식
- 예약 단위: 30분
- 보관: 취소 예약은 30일 후 정리
- 인덱스: reservations 에 (room_id, start_at, end_at) 추가

[미확정]
- 부서별 집계 화면
- 반복 예약
- 시간 표기 형식 통일 (24시간제 / 12시간제)

[참고]
회의실 개수는 총무팀 목록 기준으로 적었으나
실제 초기 적재 건수와 대조가 필요함.
'''

# ─────────────────────────────── config
F['roombook/config/app-config.yaml'] = '''# roombook 애플리케이션 설정 (실습용)

app:
  name: roombook
  version: 0.4.2
  port: 8080

business:
  openHour: 8
  closeHour: 20
  slotMinutes: 30
  maxConcurrentReservations: 5
  cancelDeadlineMinutes: 30

database:
  host: db.internal.example
  port: 5432
  name: roombook
  user: roombook_app
  # 비밀번호는 환경변수로 주입한다

logging:
  level: info
  auditTable: audit_log
'''

F['roombook/config/env.example.txt'] = '''# .env 예시 파일 — 실제 값은 넣지 않는다
# 배포 시 이 파일을 복사해 .env 로 만들고 값을 채운다

ROOMBOOK_DB_HOST=db.internal.example
ROOMBOOK_DB_PORT=5432
ROOMBOOK_DB_NAME=roombook
ROOMBOOK_DB_USER=roombook_app
ROOMBOOK_DB_PASS=<여기에_비밀번호>

ROOMBOOK_API_BASE=https://roombook.internal.example/api/v2
ROOMBOOK_MAIL_FROM=noreply@example.com
'''

F['roombook/config/deploy/docker-compose.yml'] = '''# roombook 배포 구성 (실습용)

version: "3.8"

services:
  api:
    image: roombook/api:0.4.2
    ports:
      - "8080:8080"
    environment:
      - ROOMBOOK_DB_HOST=db
      - ROOMBOOK_DB_USER=roombook_app
      - ROOMBOOK_DB_PASS=P@ssw0rd!2026
      - NODE_ENV=production
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=roombook
      - POSTGRES_USER=roombook_app
      - POSTGRES_PASSWORD=P@ssw0rd!2026
    volumes:
      - dbdata:/var/lib/postgresql/data

volumes:
  dbdata:
'''

F['roombook/config/deploy/scripts/health-check.sh'] = '''#!/bin/sh
# roombook 헬스체크 — 배포 후 상태 확인용

HOST="${1:-http://localhost:8080}"
RETRY=10
SLEEP=3

echo "health check -> $HOST/healthz"

i=1
while [ "$i" -le "$RETRY" ]; do
  if curl -fsS "$HOST/healthz" > /dev/null 2>&1; then
    echo "ok ($i번째 시도)"
    exit 0
  fi
  echo "  대기중... ($i/$RETRY)"
  i=$((i + 1))
  sleep "$SLEEP"
done

echo "실패: $RETRY번 시도해도 응답 없음"
exit 1
'''


def main():
    for rel, body in F.items():
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with io.open(path, 'w', encoding='utf-8') as fh:
            fh.write(body)

    # 검증
    names, depths, exts, dirs_with_files = {}, [], {}, set()
    dup = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel = os.path.relpath(dirpath, os.path.dirname(ROOT))
        depth = len(rel.split(os.sep))
        if filenames:
            dirs_with_files.add(rel)
        for fn in filenames:
            depths.append((depth, os.path.join(rel, fn)))
            if fn in names:
                dup.append(fn)
            names[fn] = rel
            exts[os.path.splitext(fn)[1] or '(없음)'] = exts.get(os.path.splitext(fn)[1] or '(없음)', 0) + 1

    all_dirs = set()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        all_dirs.add(os.path.relpath(dirpath, os.path.dirname(ROOT)))
    empty = sorted(all_dirs - dirs_with_files)

    print(f'파일 {len(names)}개 · 폴더 {len(all_dirs)}개')
    print(f'최대 뎁스 {max(d for d, _ in depths)} — 예: {max(depths)[1]}')
    print(f'중복 파일명: {dup or "없음"}')
    print(f'파일 없는 폴더: {empty or "없음"}')
    print('확장자:', dict(sorted(exts.items(), key=lambda x: -x[1])))

    # 배포용 zip
    zpath = ROOT + '.zip'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for dirpath, _, filenames in os.walk(ROOT):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                z.write(full, os.path.relpath(full, os.path.dirname(ROOT)))
    print(f'zip: {os.path.getsize(zpath)/1024:.0f} KB')


if __name__ == '__main__':
    main()
