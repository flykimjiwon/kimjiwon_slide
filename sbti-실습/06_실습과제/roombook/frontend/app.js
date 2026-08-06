// roombook 프론트엔드 진입점

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
