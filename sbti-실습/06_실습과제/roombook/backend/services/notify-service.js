// 알림 서비스 — 사내 메일/메신저 발송 (실습용 스텁)

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
