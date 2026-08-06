// 달력 위젯 — 날짜별 회의실 가용 슬롯을 그린다

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
