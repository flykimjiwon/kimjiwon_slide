-- 002 되돌리기
-- 인덱스 생성이 운영 중 잠금을 유발할 때만 실행한다. 평상시에는 실행하지 않는다.

BEGIN;

DROP INDEX IF EXISTS idx_reservations_room_time;
DROP INDEX IF EXISTS idx_reservations_emp;

COMMIT;
