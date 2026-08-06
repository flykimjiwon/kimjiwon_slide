-- ============================================================================
--  [SQL 실습 B]  관리자 이용률 리포트가 30초 걸린다
-- ============================================================================
--
--  상황
--    관리자 대시보드(frontend/pages/admin/dashboard-panel.html)가 열릴 때
--    아래 쿼리를 부른다. 회의실 7개짜리 화면인데 30초가 걸린다.
--    회의실을 20개로 늘리면 더 느려질 것이 뻔하다.
--
--  현재 인덱스
--    reservations : PK(id)
--                   idx_reservations_room_time  (room_id, start_at, end_at)
--                   idx_reservations_emp        (emp_no)
--    audit_log    : PK(id)  ← 그 외 인덱스 없음
--    users        : PK(emp_no), idx_users_dept (dept)
--
--  EXPLAIN ANALYZE 요약  (B-1)
--    Seq Scan on rooms  (rows=7)
--      SubPlan 1 -> Aggregate -> Seq Scan on reservations  (실행 7회)
--      SubPlan 2 -> Aggregate -> Seq Scan on reservations  (실행 7회)
--      SubPlan 3 -> Aggregate -> Seq Scan on reservations  (실행 7회)
--    Execution Time: 30188.402 ms
--
--    → 회의실 1개마다 reservations 전체를 3번씩 훑는다. 7 x 3 = 21회 풀스캔.
--
--  과제
--    B-1 : 서브쿼리 3개를 없애고 한 번만 훑도록 다시 쓰시오.
--    B-2 : 인덱스 관점에서 무엇이 빠져 있는지 찾고, 쿼리에서 불필요한 부분을 지우시오.
--
-- ============================================================================


-- ▼ B-1  회의실별 이용 현황 (문제 쿼리)

SELECT
    m.code,
    m.name,
    (SELECT COUNT(*)
       FROM reservations x
      WHERE x.room_id = m.code
        AND x.status = 'CONFIRMED')                                AS total_cnt,
    (SELECT COUNT(DISTINCT x.emp_no)
       FROM reservations x
      WHERE x.room_id = m.code)                                    AS user_cnt,
    (SELECT SUM(EXTRACT(EPOCH FROM (x.end_at - x.start_at)) / 60)
       FROM reservations x
      WHERE x.room_id = m.code
        AND x.status = 'CONFIRMED')                                AS used_minutes
FROM rooms m
WHERE m.active = true
ORDER BY used_minutes DESC;


-- ▼ B-2  최근 30일 감사로그 집계 (문제 쿼리)

SELECT a.actor,
       u.name,
       u.dept,
       COUNT(*) AS action_cnt
FROM audit_log a, users u
WHERE a.actor = u.emp_no
  AND a.created_at >= NOW() - INTERVAL '30 days'
GROUP BY a.actor, u.name, u.dept
HAVING COUNT(*) > 0
ORDER BY action_cnt DESC;


-- ============================================================================
--  스스로 점검할 질문
--
--   B-1
--    1. 같은 테이블(reservations)을 세 번 따로 세고 있다. 한 번에 셀 수 없는가?
--    2. LEFT JOIN + GROUP BY 로 바꾸면 서브쿼리 3개가 몇 개로 줄어드는가?
--    3. status 조건이 붙은 집계와 안 붙은 집계가 섞여 있다.
--       JOIN 으로 합칠 때 이 둘을 어떻게 구분해야 하는가?
--       (힌트: COUNT(*) FILTER (WHERE ...) 또는 SUM(CASE WHEN ... THEN 1 ELSE 0 END))
--    4. 예약이 하나도 없는 회의실도 결과에 나와야 한다. INNER JOIN 이면 어떻게 되는가?
--
--   B-2
--    5. audit_log 에는 어떤 인덱스가 있는가? created_at 으로 거르는데 괜찮은가?
--    6. HAVING COUNT(*) > 0 은 무슨 일을 하는가? 없어도 결과가 같은가?
--    7. FROM a, b + WHERE 조인을 명시적 JOIN 으로 바꾸면 무엇이 좋아지는가?
--
--  제출물 : 고쳐 쓴 쿼리 2개 + 추가로 만들어야 할 인덱스 CREATE 문
-- ============================================================================
