-- ────────────────────────────────────────────────────────────────────────────
--  ※ 전부 가상입니다. 은행명·고객명·계좌번호·상품명·수치 모두 지어낸 값이며
--     실제 상품·고객·시스템과 아무 관련이 없습니다. 교육 실습 전용입니다.
-- ────────────────────────────────────────────────────────────────────────────

-- ════════════════════════════════════════════════════════════════════════
--  [문제 2] 상품별 가입현황 집계가 30초 걸린다     ★★★   ← "전(前)"
-- ════════════════════════════════════════════════════════════════════════
--
--  상황
--    수신상품 대시보드가 열릴 때마다 이 쿼리를 부른다.
--    상품이 7개뿐인데 30초가 걸린다. 상품을 40개로 늘리면 답이 없다.
--
--  현재 인덱스
--    account  : PK(acct_no), idx_account_cust (cust_no)
--               ※ prod_cd 에는 인덱스가 없다
--    product  : PK(prod_cd)
--    customer : PK(cust_no), idx_customer_grade (grade)
--
--  EXPLAIN ANALYZE 요약
--    Seq Scan on product  (rows=7)
--      SubPlan 1 -> Aggregate -> Seq Scan on account   (실행 7회)
--      SubPlan 2 -> Aggregate -> Seq Scan on account   (실행 7회)
--      SubPlan 3 -> Aggregate -> Seq Scan on account   (실행 7회)
--    Execution Time: 30188.402 ms
--
--    → 상품 1건마다 account 전체를 3번씩 훑는다. 7 x 3 = 21회 풀스캔.
--
--  업무 요건 (중요)
--    · 판매중지 상품이라도 목록에 나와야 한다
--    · 가입 계좌가 0건인 상품도 0으로 표시되어야 한다   ← 놓치기 쉽다
--
--  과제
--    ① 서브쿼리 3개를 없애고 account 를 한 번만 읽도록 다시 쓰시오.
--    ② 추가로 만들어야 할 인덱스를 제시하시오.
--
-- ════════════════════════════════════════════════════════════════════════


SELECT
    p.prod_cd,
    p.prod_nm,
    p.prod_type,
    (SELECT COUNT(*)
       FROM account a
      WHERE a.prod_cd = p.prod_cd
        AND a.status = 'NORMAL')                        AS 정상계좌수,
    (SELECT COUNT(DISTINCT a.cust_no)
       FROM account a
      WHERE a.prod_cd = p.prod_cd)                      AS 가입고객수,
    (SELECT SUM(a.balance)
       FROM account a
      WHERE a.prod_cd = p.prod_cd
        AND a.status = 'NORMAL')                        AS 총잔액
FROM product p
GROUP BY p.prod_cd, p.prod_nm, p.prod_type
HAVING COUNT(*) > 0
ORDER BY 총잔액 DESC;


-- ────────────────────────────────────────────────────────────────────────
--  스스로 점검할 질문
--    1. 같은 테이블(account)을 세 번 따로 세고 있다. 한 번에 셀 수 없는가?
--    2. JOIN 으로 바꿀 때 INNER JOIN 을 쓰면 「가입 0건 상품」은 어떻게 되는가?
--    3. status 조건이 붙은 집계와 안 붙은 집계가 섞여 있다. 어떻게 구분하는가?
--       (힌트: COUNT(*) FILTER (WHERE ...) 또는 SUM(CASE WHEN ... THEN 1 ELSE 0 END))
--    4. HAVING COUNT(*) > 0 은 무슨 일을 하는가? 없으면 결과가 달라지는가?
--    5. account.prod_cd 로 매번 조인·집계하는데 인덱스가 없다. 무엇을 만들어야 하는가?
--
--  다 풀었으면 02-상품가입현황_최적화.sql 과 비교해보세요.
-- ────────────────────────────────────────────────────────────────────────
