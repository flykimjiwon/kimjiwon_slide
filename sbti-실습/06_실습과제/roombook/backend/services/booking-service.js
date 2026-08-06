// 예약 서비스 — 겹침 검사와 저장

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
