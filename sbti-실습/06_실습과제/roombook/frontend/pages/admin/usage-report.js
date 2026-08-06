// 관리자 — 회의실 이용률 리포트

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
