-- ────────────────────────────────────────────────────────────────────────────
--  ※ 전부 가상입니다. 페이지명·수치 모두 지어낸 값.
-- ────────────────────────────────────────────────────────────────────────────
-- [문제 2 정답] 앱 페이지별 PV·UV 집계 — Oracle · MySQL 8 공통 문법
--   검증된 결과: 20행 / LIMIT 을 떼면 988행 (그중 PV=0 이 376행)

SELECT p.page_cd  AS 페이지코드,
       p.page_nm  AS 페이지명,
       p.category AS 카테고리,
       COUNT(l.log_id)              AS PV,          -- COUNT(*) 아님!
       COUNT(DISTINCT l.cust_no)    AS UV,          -- NULL(비로그인) 자동 제외
       COUNT(DISTINCT l.session_id) AS 세션수,
       COALESCE(ROUND(AVG(l.stay_sec), 1), 0) AS 평균체류초
FROM app_page p
LEFT JOIN page_view_log l
       ON l.page_id  = p.page_id
      AND l.view_at >= TIMESTAMP '2026-07-01 00:00:00'   -- ★ 기간 조건은 ON 절에
      AND l.view_at <  TIMESTAMP '2026-08-01 00:00:00'
WHERE p.close_dt IS NULL
   OR p.close_dt >= DATE '2026-07-01'
GROUP BY p.page_cd, p.page_nm, p.category, p.page_id
ORDER BY PV DESC, p.page_id
LIMIT 20;                       -- Oracle 은 이 줄을  FETCH FIRST 20 ROWS ONLY  로

-- 함정 요약
--  ① 기간 조건을 WHERE 에 두면 LEFT JOIN 이 INNER 처럼 동작 → 988행이 612행으로 (376개 소실)
--     상위 20개는 정답과 똑같이 나와서 눈으로는 못 잡는다.
--  ② COUNT(*) 를 쓰면 조회 0건 페이지가 PV=1 로 나온다 → COUNT(l.log_id)
--  ③ 로그 없는 페이지의 AVG 는 NULL → COALESCE(...,0)
-- 검증법: LIMIT 을 떼고 COUNT 하면 988, PV=0 인 행이 376 이어야 한다.
