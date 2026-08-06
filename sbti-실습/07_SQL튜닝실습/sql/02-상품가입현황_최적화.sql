-- ────────────────────────────────────────────────────────────────────────────
--  ※ 전부 가상입니다. 은행명·고객명·계좌번호·상품명·수치 모두 지어낸 값이며
--     실제 상품·고객·시스템과 아무 관련이 없습니다. 교육 실습 전용입니다.
-- ────────────────────────────────────────────────────────────────────────────

-- ════════════════════════════════════════════════════════════════════════
--  [문제 2 정답] 상품별 가입현황 집계        ← "후(後)"
--  실행시간  30188 ms  →  38 ms   (약 790배)
-- ════════════════════════════════════════════════════════════════════════
--
--  고친 것
--
--   ① 상관 서브쿼리 3개  →  LEFT JOIN 1번 + GROUP BY
--      account 를 21번 훑던 것을 1번으로 줄인다. 이게 대부분의 시간을 잡아먹었다.
--
--   ② LEFT JOIN 이어야 한다 (INNER 아님)
--      '참좋은 파킹통장'(P007)은 가입 계좌가 0건이다.
--      INNER JOIN 으로 바꾸면 이 상품이 목록에서 사라진다. 업무 요건 위반.
--
--   ③ status 조건은 FILTER 로 구분
--      정상계좌수·총잔액은 status='NORMAL' 만, 가입고객수는 전체가 대상이다.
--      WHERE 로 걸면 세 집계 전부에 적용돼 버린다.
--
--   ④ COALESCE 로 NULL → 0
--      가입 0건 상품의 SUM 은 NULL 이 된다. 화면에 빈칸이 아니라 0 이 나와야 한다.
--
--   ⑤ HAVING COUNT(*) > 0 삭제
--      GROUP BY 결과에 0건짜리 그룹은 애초에 존재하지 않는다. 무의미한 조건이었다.
--      오히려 LEFT JOIN 후에는 이 조건이 0건 상품을 걸러낼 위험이 있다.
--
--   ⑥ 인덱스 추가  ← 쿼리만 고치면 절반이다
--
--  EXPLAIN ANALYZE 요약
--    HashAggregate
--      -> Hash Right Join
--         -> Index Scan using idx_account_prod on account
--         -> Seq Scan on product (rows=7)
--    Execution Time: 38.771 ms
--
-- ════════════════════════════════════════════════════════════════════════


-- ▼ 먼저 인덱스부터 만든다
CREATE INDEX idx_account_prod ON account (prod_cd);
-- 정상계좌만 자주 본다면 부분 인덱스가 더 낫다
-- CREATE INDEX idx_account_prod_normal ON account (prod_cd) WHERE status = 'NORMAL';


-- ▼ 고친 쿼리

SELECT
    p.prod_cd,
    p.prod_nm,
    p.prod_type,
    COUNT(*) FILTER (WHERE a.status = 'NORMAL')                        AS 정상계좌수,
    COUNT(DISTINCT a.cust_no)                                          AS 가입고객수,
    COALESCE(SUM(a.balance) FILTER (WHERE a.status = 'NORMAL'), 0)     AS 총잔액
FROM product p
LEFT JOIN account a ON a.prod_cd = p.prod_cd
GROUP BY p.prod_cd, p.prod_nm, p.prod_type
ORDER BY 총잔액 DESC;


-- ────────────────────────────────────────────────────────────────────────
--  FILTER 를 못 쓰는 DBMS 라면 CASE 로 같은 결과를 낸다
--
--    SUM(CASE WHEN a.status = 'NORMAL' THEN 1 ELSE 0 END)        AS 정상계좌수,
--    COALESCE(SUM(CASE WHEN a.status = 'NORMAL'
--                      THEN a.balance ELSE 0 END), 0)            AS 총잔액
--
--  검증 방법
--    · 결과 행 수가 상품 수(7)와 같은지 확인한다. 6이면 LEFT JOIN 이 안 된 것이다.
--    · P007 '참좋은 파킹통장' 이 0 / 0 / 0 으로 나오는지 확인한다.
-- ────────────────────────────────────────────────────────────────────────
