-- ────────────────────────────────────────────────────────────────────────────
--  ※ 전부 가상입니다. 은행명·직원명·사번·영업점·상품명·수치 모두 지어낸 값.
-- ────────────────────────────────────────────────────────────────────────────
-- [문제 1 정답] 카드 가입권유 실적 상위 10명 — Oracle · MySQL 8 공통 문법
--   (WITH / CASE WHEN / RANK() OVER / NULLIF / ROUND 만 사용. FILTER 등 전용 문법 없음)
--   검증된 결과: 12행 (공동 1위 2명 · 공동 10위 3명)

WITH agg AS (
    SELECT r.ref_emp_no,
           SUM(CASE WHEN r.ref_status = 'NORMAL'    THEN 1 ELSE 0 END) AS 추천건수,
           COUNT(DISTINCT CASE WHEN r.ref_status = 'NORMAL'
                               THEN r.cust_no END)                     AS 추천고객수,
           SUM(CASE WHEN r.ref_status = 'CANCELLED' THEN 1 ELSE 0 END) AS 취소건수
    FROM referral r
    JOIN product  p ON p.prod_cd = r.prod_cd
    JOIN employee e ON e.emp_no  = r.ref_emp_no
    WHERE p.prod_type  = 'CARD'
      AND e.emp_status = '재직'                 -- 순위 매기기 "전"에 제외
      AND r.apply_dt  >= DATE '2026-01-01'
      AND r.apply_dt  <  DATE '2026-07-01'      -- < 7월 1일 (<= 6월 30일 아님)
    GROUP BY r.ref_emp_no
),
ranked AS (
    SELECT agg.*, RANK() OVER (ORDER BY 추천건수 DESC) AS 순위
    FROM agg
    WHERE 추천건수 > 0
)
SELECT r.순위,
       r.ref_emp_no AS 사번,
       e.emp_nm     AS 직원명,
       b.branch_nm  AS 영업점명,
       e.position   AS 직급,
       r.추천건수, r.추천고객수, r.취소건수,
       ROUND(r.취소건수 * 100.0 / NULLIF(r.추천건수 + r.취소건수, 0), 1) AS "취소율(%)"
FROM ranked r
JOIN employee e ON e.emp_no    = r.ref_emp_no
JOIN branch   b ON b.branch_cd = e.branch_cd
WHERE r.순위 <= 10
ORDER BY r.순위, r.추천고객수 DESC, r.ref_emp_no;

-- 함정 요약
--  ① "상위 10명"을 LIMIT/FETCH FIRST 로 자르면 공동 10위 3명 중 일부가 잘린다 → RANK 후 순위<=10
--  ② 재직 필터를 집계 뒤로 미루면 순위에 구멍이 생긴다 (3위 퇴직자 남해린)
--  ③ WHERE ref_status='NORMAL' 로 걸면 취소건수를 셀 수 없다 → CASE WHEN 으로 동시 집계
--  ④ 취소율 분모 0 → NULLIF
-- Oracle 참고: DATE '2026-01-01' 은 ANSI 리터럴로 Oracle·MySQL 모두 지원.
