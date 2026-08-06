-- ============================================================================
--  [SQL 실습 A]  "내 예약" 조회가 4초 걸린다
-- ============================================================================
--
--  상황
--    예약 30만 건이 쌓인 뒤로 "내 예약" 화면과 관리자 검색이 눈에 띄게 느려졌다.
--    인덱스는 이미 만들어 뒀는데도 실행계획에 Seq Scan 이 찍힌다.
--
--  현재 인덱스  (database/schema.sql, database/migrations/002-add-index.sql)
--    reservations : PK(id)
--                   idx_reservations_room_time  (room_id, start_at, end_at)
--                   idx_reservations_emp        (emp_no)
--    rooms        : PK(id), UNIQUE(code), idx_rooms_floor (floor)
--    users        : PK(emp_no), idx_users_dept (dept)
--
--  컬럼 타입  (헷갈리기 쉬우니 확인할 것)
--    reservations.emp_no    VARCHAR(7)     -- 숫자처럼 보이지만 문자열이다
--    reservations.room_id   VARCHAR(10)    -- rooms.code 를 참조한다
--    reservations.start_at  TIMESTAMP
--    reservations.end_at    TIMESTAMP
--    reservations.status    VARCHAR(12)    -- 'CONFIRMED' | 'PENDING' | 'CANCELLED'
--
--  EXPLAIN ANALYZE 요약
--    Seq Scan on reservations  (cost=0.00..18420.00 rows=1 width=96)
--      Filter: (date(start_at) = '2026-08-10'::date)
--      Rows Removed by Filter: 299873
--    Planning Time: 0.412 ms
--    Execution Time: 4213.877 ms
--
--  과제
--    아래 쿼리가 인덱스를 못 쓰는 이유를 찾고 다시 작성하시오.
--    원인은 하나가 아니다. 최소 4가지를 찾을 수 있다.
--
--  화면에서 실제로 필요한 컬럼
--    예약ID · 회의실코드 · 회의실명 · 시작 · 종료 · 목적 · 상태
--
-- ============================================================================


-- ▼ 문제 쿼리 (이대로 운영에 나가 있다)

SELECT *
FROM reservations r
WHERE DATE(r.start_at) = '2026-08-10'
  AND r.emp_no = 1234567
  AND (r.status = 'CONFIRMED' OR r.status = 'PENDING')
  AND r.purpose LIKE '%회의%'
ORDER BY r.start_at DESC;


-- ▼ 참고 : 회의실 이름까지 붙여 내려주는 버전. 여기도 같은 문제가 있다.

SELECT *
FROM reservations r, rooms m
WHERE r.room_id = m.code
  AND DATE(r.start_at) BETWEEN '2026-08-01' AND '2026-08-31'
  AND UPPER(r.status) = 'CONFIRMED'
ORDER BY r.start_at DESC;


-- ============================================================================
--  스스로 점검할 질문 (막히면 하나씩 AI에게 물어보세요)
--
--    1. 인덱스가 걸린 컬럼을 DATE() 로 감싸면 인덱스를 쓸 수 있는가?
--    2. emp_no 는 VARCHAR 인데 1234567 로 비교하면 무슨 일이 일어나는가?
--    3. SELECT * 는 위 "필요한 컬럼" 목록과 비교해 얼마나 낭비인가?
--    4. LIKE '%...%' 처럼 앞에 % 가 붙으면 인덱스를 탈 수 있는가?
--    5. 두 번째 쿼리의 콤마 조인(FROM a, b)은 왜 권장되지 않는가?
--
--  제출물 : 고쳐 쓴 쿼리 + 왜 빨라지는지 한 줄 설명
-- ============================================================================
