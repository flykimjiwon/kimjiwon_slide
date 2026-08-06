-- 002 : 예약 조회 성능 개선
-- 적용일 2026-07-02
-- 배경: 내 예약 목록 조회가 느리다는 접수 (2026-07-03 중간점검 참고)

BEGIN;

CREATE INDEX idx_reservations_room_time ON reservations (room_id, start_at, end_at);
CREATE INDEX idx_reservations_emp ON reservations (emp_no);

COMMIT;
