#!/usr/bin/env python3
"""07_SQL튜닝실습 — 가상 은행 테마 SQL 전/후 비교 실습 생성."""
import io, os, zipfile

ROOT = '/Users/kimjiwon/Desktop/SBTI_PDF_모음_2026-08-05/07_SQL튜닝실습'
F = {}

BANNER = """-- ────────────────────────────────────────────────────────────────────────────
--  ※ 전부 가상입니다. 은행명·고객명·계좌번호·상품명·수치 모두 지어낸 값이며
--     실제 상품·고객·시스템과 아무 관련이 없습니다. 교육 실습 전용입니다.
-- ────────────────────────────────────────────────────────────────────────────
"""

# ══════════════════════════════════════════════ 스키마
F['schema/한빛은행_스키마_샘플데이터.sql'] = BANNER + '''
-- 가상 은행 「한빛은행」 수신 시스템 (실습용 축약 스키마)

DROP TABLE IF EXISTS txn, account, product, customer;

-- 고객 ------------------------------------------------------------------
CREATE TABLE customer (
    cust_no    VARCHAR(10) PRIMARY KEY,      -- C0000001
    cust_nm    VARCHAR(30)  NOT NULL,
    birth_ymd  CHAR(8),
    join_dt    DATE         NOT NULL,
    grade      VARCHAR(10)  NOT NULL         -- BASIC | GOLD | VIP
);
CREATE INDEX idx_customer_grade ON customer (grade);

-- 상품 ------------------------------------------------------------------
CREATE TABLE product (
    prod_cd    VARCHAR(8)  PRIMARY KEY,      -- P001
    prod_nm    VARCHAR(60) NOT NULL,
    prod_type  VARCHAR(10) NOT NULL,         -- DEPOSIT | SAVING | LOAN | FUND
    base_rate  NUMERIC(5,3),
    sale_yn    CHAR(1)     NOT NULL          -- Y | N
);
-- 인덱스: PK 뿐

-- 계좌 ------------------------------------------------------------------
CREATE TABLE account (
    acct_no    VARCHAR(14) PRIMARY KEY,      -- 000-000-000001
    cust_no    VARCHAR(10) NOT NULL,
    prod_cd    VARCHAR(8)  NOT NULL,
    balance    NUMERIC(18,0) NOT NULL DEFAULT 0,
    open_dt    DATE        NOT NULL,
    status     VARCHAR(10) NOT NULL          -- NORMAL | DORMANT | CLOSED
);
CREATE INDEX idx_account_cust ON account (cust_no);
-- ※ prod_cd 에는 인덱스가 없다 (실습 2번에서 다룬다)

-- 거래 ------------------------------------------------------------------
CREATE TABLE txn (
    txn_id        BIGSERIAL PRIMARY KEY,
    acct_no       VARCHAR(14)  NOT NULL,
    txn_at        TIMESTAMP    NOT NULL,
    txn_type      VARCHAR(10)  NOT NULL,     -- DEPOSIT | WITHDRAW | TRANSFER
    amount        NUMERIC(18,0) NOT NULL,
    balance_after NUMERIC(18,0) NOT NULL,
    memo          VARCHAR(60)
);
CREATE INDEX idx_txn_acct_time ON txn (acct_no, txn_at);


-- ══════════════════════════════════════════════════════════════════════
--  샘플 데이터 (전부 가상)
-- ══════════════════════════════════════════════════════════════════════

INSERT INTO customer (cust_no, cust_nm, birth_ymd, join_dt, grade) VALUES
  ('C0000001', '김하늘', '19880312', '2015-04-02', 'VIP'),
  ('C0000002', '이바다', '19950721', '2019-11-15', 'GOLD'),
  ('C0000003', '박구름', '20010109', '2023-03-08', 'BASIC'),
  ('C0000004', '최나무', '19790525', '2011-06-21', 'VIP'),
  ('C0000005', '정바람', '19930214', '2020-08-30', 'BASIC'),
  ('C0000006', '강별',   '19861130', '2014-02-17', 'GOLD'),
  ('C0000007', '윤노을', '19990403', '2022-05-11', 'BASIC');

INSERT INTO product (prod_cd, prod_nm, prod_type, base_rate, sale_yn) VALUES
  ('P001', '행복드림 자유적금',     'SAVING',  3.200, 'Y'),
  ('P002', '든든플러스 정기예금',   'DEPOSIT', 3.550, 'Y'),
  ('P003', '새싹 청년우대적금',     'SAVING',  4.100, 'Y'),
  ('P004', '한걸음 신용대출',       'LOAN',    5.800, 'Y'),
  ('P005', '미래설계 연금저축',     'FUND',    NULL,  'Y'),
  ('P006', '슬기로운 주택청약',     'SAVING',  2.800, 'Y'),
  ('P007', '참좋은 파킹통장',       'DEPOSIT', 2.100, 'N');   -- 판매중지, 가입 0건

INSERT INTO account (acct_no, cust_no, prod_cd, balance, open_dt, status) VALUES
  ('000-000-000001', 'C0000001', 'P002', 52000000, '2021-01-11', 'NORMAL'),
  ('000-000-000002', 'C0000001', 'P001',  8400000, '2022-07-04', 'NORMAL'),
  ('000-000-000003', 'C0000002', 'P003',  3120000, '2023-02-20', 'NORMAL'),
  ('000-000-000004', 'C0000003', 'P003',   940000, '2024-05-06', 'NORMAL'),
  ('000-000-000005', 'C0000004', 'P002', 98000000, '2018-09-13', 'NORMAL'),
  ('000-000-000006', 'C0000004', 'P006',  6200000, '2020-03-25', 'NORMAL'),
  ('000-000-000007', 'C0000005', 'P001',  1750000, '2023-11-02', 'DORMANT'),
  ('000-000-000008', 'C0000006', 'P004', 24000000, '2022-12-19', 'NORMAL'),
  ('000-000-000009', 'C0000007', 'P005',  5300000, '2024-01-30', 'NORMAL'),
  ('000-000-000010', 'C0000002', 'P006',  2100000, '2021-08-17', 'CLOSED');

INSERT INTO txn (acct_no, txn_at, txn_type, amount, balance_after, memo) VALUES
  ('000-000-000001', '2026-07-03 09:12:41', 'DEPOSIT',   3000000, 52000000, '급여'),
  ('000-000-000001', '2026-07-15 14:33:02', 'WITHDRAW',   500000, 51500000, '카드대금'),
  ('000-000-000002', '2026-07-04 08:01:11', 'DEPOSIT',    300000,  8400000, '자동이체 적금'),
  ('000-000-000003', '2026-07-04 08:01:12', 'DEPOSIT',    200000,  3120000, '자동이체 적금'),
  ('000-000-000005', '2026-07-09 16:47:55', 'TRANSFER',  1200000, 98000000, '이체'),
  ('000-000-000005', '2026-07-22 11:05:38', 'WITHDRAW',   800000, 97200000, '출금'),
  ('000-000-000008', '2026-07-25 10:20:07', 'WITHDRAW',   450000, 23550000, '대출이자'),
  ('000-000-000009', '2026-07-28 13:59:44', 'DEPOSIT',    150000,  5450000, '연금 납입');
'''

# ══════════════════════════════════════════════ 문제 1 — 실습본
F['sql/01-거래내역조회_실습본.sql'] = BANNER + '''
-- ════════════════════════════════════════════════════════════════════════
--  [문제 1] 거래내역 조회가 느리다        ★★     ← 이 파일이 "전(前)"
-- ════════════════════════════════════════════════════════════════════════
--
--  상황
--    인터넷뱅킹 「거래내역 조회」 화면에서 쓰는 쿼리다.
--    txn 테이블이 4,200만 건이 되면서 조회에 평균 6.8초가 걸린다.
--    인덱스는 있는데 실행계획에 Seq Scan 이 찍힌다.
--
--  현재 인덱스
--    txn      : PK(txn_id),  idx_txn_acct_time (acct_no, txn_at)
--    account  : PK(acct_no), idx_account_cust (cust_no)
--    customer : PK(cust_no), idx_customer_grade (grade)
--    product  : PK(prod_cd)
--
--  컬럼 타입 (중요)
--    txn.acct_no      VARCHAR(14)   -- '000-000-000001' 형식. 숫자가 아니다
--    txn.txn_at       TIMESTAMP
--    account.cust_no  VARCHAR(10)
--
--  EXPLAIN ANALYZE 요약
--    Seq Scan on txn  (cost=0.00..982400.00 rows=1 width=120)
--      Filter: (date(txn_at) >= '2026-07-01'::date AND date(txn_at) <= '2026-07-31'::date)
--      Rows Removed by Filter: 41,873,552
--    Execution Time: 6842.113 ms
--
--  화면에서 실제로 필요한 컬럼
--    거래일시 · 거래구분 · 금액 · 거래후잔액 · 적요 · 상품명
--
--  과제
--    인덱스를 못 쓰게 만드는 원인을 찾고 다시 작성하시오. 원인은 4가지다.
--
-- ════════════════════════════════════════════════════════════════════════


SELECT *
FROM txn t, account a, product p
WHERE t.acct_no = a.acct_no
  AND a.prod_cd = p.prod_cd
  AND DATE(t.txn_at) >= '2026-07-01'
  AND DATE(t.txn_at) <= '2026-07-31'
  AND t.acct_no = 000000000001
  AND (t.txn_type = 'DEPOSIT' OR t.txn_type = 'WITHDRAW')
  AND t.memo LIKE '%급여%'
ORDER BY t.txn_at DESC;


-- ────────────────────────────────────────────────────────────────────────
--  스스로 점검할 질문
--    1. txn_at 에 DATE() 를 씌우면 idx_txn_acct_time 을 탈 수 있는가?
--    2. acct_no 는 VARCHAR(14) 인데 000000000001 로 비교하면 어떻게 되는가?
--       (하이픈도 빠져 있다)
--    3. SELECT * 는 위 "필요한 컬럼" 6개와 비교해 얼마나 낭비인가?
--    4. LIKE '%급여%' 는 인덱스를 탈 수 있는가?
--    5. FROM a, b, c 콤마 조인은 왜 위험한가?
--
--  다 풀었으면 01-거래내역조회_최적화.sql 과 비교해보세요.
-- ────────────────────────────────────────────────────────────────────────
'''

# ══════════════════════════════════════════════ 문제 1 — 최적화
F['sql/01-거래내역조회_최적화.sql'] = BANNER + '''
-- ════════════════════════════════════════════════════════════════════════
--  [문제 1 정답] 거래내역 조회        ← 이 파일이 "후(後)"
--  실행시간  6842 ms  →  11 ms   (약 620배)
-- ════════════════════════════════════════════════════════════════════════
--
--  고친 것 4가지
--
--   ① DATE(t.txn_at) 범위 조건  →  범위 비교로 변경
--      컬럼을 함수로 감싸면 인덱스를 못 쓴다. 컬럼은 그대로 두고 값 쪽을 바꾼다.
--      끝을 '2026-07-31' 로 잡으면 그날 00:00:00 만 포함되어 하루가 통째로 빠진다.
--      그래서 "다음 달 1일 미만(<)" 으로 잡는다.  <= 가 아니라 < 인 것에 주의.
--
--   ② t.acct_no = 000000000001  →  '000-000-000001'
--      VARCHAR 컬럼에 숫자를 넣으면 암묵적 형변환이 일어나 인덱스가 죽는다.
--      게다가 하이픈이 빠져 있어 애초에 매칭되지도 않는다.
--
--   ③ SELECT *  →  화면에 필요한 6개 컬럼만
--      네트워크·메모리 절감. txn 은 컬럼이 넓어 효과가 크다.
--
--   ④ memo LIKE '%급여%'  →  조건 제거
--      선행 와일드카드는 인덱스를 못 탄다. 적요 검색이 정말 필요하면
--      애플리케이션에서 거르거나 전문검색 인덱스를 별도로 검토한다.
--
--   부가) 콤마 조인 → 명시적 JOIN. 조인 조건 누락을 눈으로 잡을 수 있다.
--        OR → IN 으로 정리.
--
--  EXPLAIN ANALYZE 요약
--    Index Scan using idx_txn_acct_time on txn
--      Index Cond: (acct_no = '000-000-000001' AND txn_at >= ... AND txn_at < ...)
--    Execution Time: 11.204 ms
--
-- ════════════════════════════════════════════════════════════════════════


SELECT t.txn_at,
       t.txn_type,
       t.amount,
       t.balance_after,
       t.memo,
       p.prod_nm
FROM txn t
JOIN account a ON a.acct_no = t.acct_no
JOIN product p ON p.prod_cd = a.prod_cd
WHERE t.acct_no = '000-000-000001'
  AND t.txn_at >= TIMESTAMP '2026-07-01 00:00:00'
  AND t.txn_at <  TIMESTAMP '2026-08-01 00:00:00'
  AND t.txn_type IN ('DEPOSIT', 'WITHDRAW')
ORDER BY t.txn_at DESC;


-- ────────────────────────────────────────────────────────────────────────
--  확인 포인트
--    · idx_txn_acct_time 은 (acct_no, txn_at) 순서다.
--      acct_no 를 = 로 고정하고 txn_at 을 범위로 주면 두 컬럼 모두 인덱스를 탄다.
--    · 조건을 뺀 memo 검색이 업무상 꼭 필요한지는 현업과 확인해야 한다.
--      "느려서 뺐다" 가 아니라 "이 조건은 인덱스로 해결이 안 된다" 로 설명할 것.
-- ────────────────────────────────────────────────────────────────────────
'''

# ══════════════════════════════════════════════ 문제 2 — 실습본
F['sql/02-상품가입현황_실습본.sql'] = BANNER + '''
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
'''

# ══════════════════════════════════════════════ 문제 2 — 최적화
F['sql/02-상품가입현황_최적화.sql'] = BANNER + '''
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
'''

# ══════════════════════════════════════════════ README
F['README.md'] = '''# SQL 튜닝 실습 — 전/후 비교

가상 은행 「한빛은행」 수신 시스템의 느린 쿼리 2개를 고쳐보는 실습입니다.

> **은행명·고객명·계좌번호·상품명·수치 전부 지어낸 값입니다.**
> 실제 상품·고객·시스템과 아무 관련이 없습니다.

## 파일

```
07_SQL튜닝실습/
├── README.md              ← 지금 보는 문서
├── 전후비교.html           같은 내용을 화면으로 (더블클릭하면 열립니다)
├── schema/
│   └── 한빛은행_스키마_샘플데이터.sql     테이블 4개 + 샘플 데이터
└── sql/
    ├── 01-거래내역조회_실습본.sql      ★★   ← 먼저 이걸 고쳐보세요
    ├── 01-거래내역조회_최적화.sql            정답
    ├── 02-상품가입현황_실습본.sql      ★★★
    └── 02-상품가입현황_최적화.sql            정답
```

`.sql` 파일은 VS Code에서 그냥 열립니다. 색도 자동으로 입혀집니다.

## 실습 방법 — 3단계

### 1단계 · 실습본만 열고 혼자 고쳐본다 (10분)

`01-거래내역조회_실습본.sql` 을 엽니다.
파일 맨 위 주석에 **상황·인덱스 목록·컬럼 타입·실행계획**이 다 적혀 있습니다.
맨 아래 「스스로 점검할 질문」을 보면서 원인을 찾아보세요.

> 최적화 파일은 아직 열지 마세요.

### 2단계 · 택가이 코드에게 물어본다

혼자 찾은 것과 AI가 찾은 것을 비교합니다.
한 번에 "최적화해줘" 하지 말고 **하나씩** 물어야 정확합니다.

```
01-거래내역조회_실습본.sql 을 읽고,
주석의 인덱스 목록과 WHERE 조건을 비교해서
인덱스를 못 타는 조건을 찾아줘
```

```
acct_no 컬럼이 VARCHAR(14) 인데 숫자로 비교하고 있어.
무슨 문제가 생기는지 알려줘
```

```
찾은 문제를 반영해서 쿼리를 다시 써줘.
컬럼은 주석의 "화면에서 실제로 필요한 컬럼" 만 써줘
```

### 3단계 · 최적화 파일과 맞춰본다

`01-거래내역조회_최적화.sql` 을 엽니다.
정답 쿼리와 **왜 그렇게 고쳤는지가 번호별로** 적혀 있습니다.

VS Code에서 두 파일을 나란히 보려면
왼쪽 탐색기에서 `실습본` 클릭 → `최적화` **⌘+클릭** 하면 좌우로 열립니다.

---

## 한눈에 보는 전/후

### 문제 1 — 거래내역 조회 · 6842ms → 11ms

| | 전 | 후 |
|---|---|---|
| 날짜 조건 | `DATE(txn_at) >= '2026-07-01'` | `txn_at >= '2026-07-01 00:00:00'` |
| 계좌번호 | `acct_no = 000000000001` | `acct_no = '000-000-000001'` |
| 조회 컬럼 | `SELECT *` | 필요한 6개만 |
| 적요 검색 | `memo LIKE '%급여%'` | 조건 제거 |
| 조인 | `FROM a, b, c` | `JOIN ... ON` |

### 문제 2 — 상품별 가입현황 · 30188ms → 38ms

| | 전 | 후 |
|---|---|---|
| 집계 방식 | 상관 서브쿼리 3개 (21회 풀스캔) | `LEFT JOIN` 1번 + `GROUP BY` |
| 조인 종류 | — | **`LEFT`** (가입 0건 상품이 사라지면 안 됨) |
| 조건별 집계 | 서브쿼리마다 WHERE | `FILTER (WHERE ...)` |
| NULL 처리 | 없음 | `COALESCE(..., 0)` |
| `HAVING COUNT(*) > 0` | 있음 (무의미) | 삭제 |
| 인덱스 | `account.prod_cd` 없음 | `idx_account_prod` 추가 |

---

## AI 답을 그대로 믿지 마세요

온프레미스 모델(Qwen3.6-35B)이 자주 틀리는 지점입니다. 직접 확인하세요.

| 확인할 것 | 왜 |
|---|---|
| **날짜 경계** | `< 다음달 1일` 이어야 하는데 `<= 말일` 로 쓰면 **마지막 날이 통째로 빠집니다** |
| **`LEFT` 인지 `INNER` 인지** | INNER 로 바꾸면 가입 0건 상품이 조용히 사라집니다 |
| **결과 건수** | 문제 2는 상품 7개가 전부 나와야 합니다. 6개면 조인이 틀린 것입니다 |
| **인덱스 생성문** | 쿼리만 고치고 `CREATE INDEX` 를 빼먹는 경우가 가장 많습니다 |

고친 쿼리를 받았으면 **"왜 빨라지는지 한 줄로 설명해줘"** 를 꼭 물어보세요.
설명을 못 하면 그 답은 못 믿습니다.
'''

# ══════════════════════════════════════════════ HTML
F['전후비교.html'] = '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SQL 튜닝 실습 — 전/후 비교</title>
<style>
:root{--blue:#0066cc;--line:#e2e7ee;--muted:#5f6672;--bad:#dc2626;--good:#16a34a;
--mono:ui-monospace,SFMono-Regular,Menlo,monospace;
--font:-apple-system,BlinkMacSystemFont,"Pretendard","Segoe UI",sans-serif}
*{box-sizing:border-box}
body{margin:0;padding:38px 26px 60px;background:#f7f9fc;color:#1a1a1a;font-family:var(--font);line-height:1.6}
.wrap{max-width:1180px;margin:0 auto}
h1{font-size:30px;letter-spacing:-.03em;margin:0 0 6px}
.sub{color:var(--muted);margin:0 0 10px}
.warn{background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;border-radius:12px;
padding:11px 16px;font-size:14px;font-weight:700;margin:0 0 30px}
h2{font-size:21px;margin:38px 0 4px;letter-spacing:-.02em}
h2 em{font-style:normal;font:800 12px var(--mono);color:#fff;background:var(--blue);
border-radius:999px;padding:4px 10px;margin-right:9px;vertical-align:3px}
.time{color:var(--muted);font-size:14px;margin:0 0 14px}
.time b{color:var(--good);font-size:16px}
.time s{color:var(--bad);text-decoration:none}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.box{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}
.box.before{border-color:#fecaca}
.box.after{border-color:#bbf7d0}
.box h3{margin:0;padding:10px 15px;font-size:13px;font-weight:900;letter-spacing:.02em}
.box.before h3{background:#fef2f2;color:#b91c1c}
.box.after h3{background:#f0fdf4;color:#15803d}
pre{margin:0;padding:15px;font:600 12.5px/1.62 var(--mono);overflow-x:auto;white-space:pre}
.hl-bad{background:#fee2e2;border-radius:3px;padding:1px 2px}
.hl-good{background:#dcfce7;border-radius:3px;padding:1px 2px}
table{border-collapse:collapse;width:100%;margin-top:16px;font-size:14px;background:#fff}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}
th{background:#f4f7fb;font-weight:800;white-space:nowrap}
td code{font:600 12px var(--mono);background:#f4f7fb;border-radius:4px;padding:1px 5px}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}
.step{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.step b{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:8px;
background:var(--blue);color:#fff;font:900 13px var(--mono);margin-bottom:9px}
.step p{margin:0;font-size:14px;color:#374151}
.step code{display:block;margin-top:9px;background:#0f172a;color:#dbeafe;border-radius:9px;
padding:10px 12px;font:600 11.5px/1.5 var(--mono);white-space:pre-wrap}
.check{background:#fff;border:1px solid var(--line);border-radius:14px;padding:6px 20px;margin-top:14px}
.foot{margin-top:44px;padding-top:16px;border-top:1px solid var(--line);
color:var(--muted);font-size:13px}
@media (max-width:860px){.pair,.steps{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="wrap">

<h1>SQL 튜닝 실습 — 전/후 비교</h1>
<p class="sub">가상 은행 「한빛은행」 수신 시스템 · 느린 쿼리 2개 고치기</p>
<p class="warn">※ 은행명 · 고객명 · 계좌번호 · 상품명 · 수치 전부 지어낸 값입니다. 실제 상품·고객·시스템과 무관합니다.</p>

<h2><em>실습 방법</em>3단계</h2>
<div class="steps">
  <div class="step"><b>1</b>
    <p>실습본만 열고 <strong>혼자</strong> 고쳐봅니다. 파일 위쪽 주석에 상황·인덱스·실행계획이 다 있습니다.</p>
    <code>sql/01-거래내역조회_실습본.sql</code></div>
  <div class="step"><b>2</b>
    <p>택가이 코드에게 <strong>하나씩</strong> 물어봅니다. 한 번에 "최적화해줘"는 금물.</p>
    <code>주석의 인덱스 목록과 WHERE 조건을
비교해서 인덱스를 못 타는
조건을 찾아줘</code></div>
  <div class="step"><b>3</b>
    <p>최적화 파일과 맞춰봅니다. VS Code에서 <strong>⌘+클릭</strong>하면 좌우로 열립니다.</p>
    <code>sql/01-거래내역조회_최적화.sql</code></div>
</div>

<h2><em>문제 1</em>거래내역 조회 <span style="font-weight:400;font-size:15px;color:#5f6672">★★</span></h2>
<p class="time"><s>6,842 ms</s> &nbsp;→&nbsp; <b>11 ms</b> &nbsp;(약 620배)</p>
<div class="pair">
  <div class="box before"><h3>전 — 실습본</h3><pre>SELECT <span class="hl-bad">*</span>
FROM <span class="hl-bad">txn t, account a, product p</span>
WHERE t.acct_no = a.acct_no
  AND a.prod_cd = p.prod_cd
  AND <span class="hl-bad">DATE(t.txn_at)</span> &gt;= '2026-07-01'
  AND <span class="hl-bad">DATE(t.txn_at)</span> &lt;= '2026-07-31'
  AND t.acct_no = <span class="hl-bad">000000000001</span>
  AND (t.txn_type = 'DEPOSIT'
    OR t.txn_type = 'WITHDRAW')
  AND t.memo LIKE <span class="hl-bad">'%급여%'</span>
ORDER BY t.txn_at DESC;</pre></div>
  <div class="box after"><h3>후 — 최적화</h3><pre>SELECT <span class="hl-good">t.txn_at, t.txn_type, t.amount,
       t.balance_after, t.memo, p.prod_nm</span>
FROM txn t
<span class="hl-good">JOIN</span> account a <span class="hl-good">ON</span> a.acct_no = t.acct_no
<span class="hl-good">JOIN</span> product p <span class="hl-good">ON</span> p.prod_cd = a.prod_cd
WHERE t.acct_no = <span class="hl-good">'000-000-000001'</span>
  AND <span class="hl-good">t.txn_at &gt;= TIMESTAMP '2026-07-01 00:00:00'</span>
  AND <span class="hl-good">t.txn_at &lt;  TIMESTAMP '2026-08-01 00:00:00'</span>
  AND t.txn_type <span class="hl-good">IN ('DEPOSIT','WITHDRAW')</span>
ORDER BY t.txn_at DESC;</pre></div>
</div>
<table>
  <tr><th>바뀐 것</th><th>전</th><th>후</th><th>왜</th></tr>
  <tr><td>날짜 조건</td><td><code>DATE(txn_at) &gt;= …</code></td><td><code>txn_at &gt;= …</code></td>
      <td>컬럼을 함수로 감싸면 인덱스를 못 탄다. 끝은 <code>&lt; 다음달 1일</code> (<code>&lt;= 말일</code>이면 마지막 날이 빠짐)</td></tr>
  <tr><td>계좌번호</td><td><code>= 000000000001</code></td><td><code>= '000-000-000001'</code></td>
      <td><code>VARCHAR(14)</code>에 숫자 비교 → 암묵적 형변환으로 인덱스 무력화. 하이픈도 빠져 있었다</td></tr>
  <tr><td>조회 컬럼</td><td><code>SELECT *</code></td><td>필요한 6개</td><td>txn은 컬럼이 넓다. 네트워크·메모리 낭비</td></tr>
  <tr><td>적요 검색</td><td><code>LIKE '%급여%'</code></td><td>제거</td><td>선행 <code>%</code>는 인덱스 사용 불가. 필요하면 별도 검토</td></tr>
  <tr><td>조인</td><td><code>FROM a, b, c</code></td><td><code>JOIN … ON</code></td><td>조인 조건 누락을 눈으로 잡을 수 있다</td></tr>
</table>

<h2><em>문제 2</em>상품별 가입현황 집계 <span style="font-weight:400;font-size:15px;color:#5f6672">★★★</span></h2>
<p class="time"><s>30,188 ms</s> &nbsp;→&nbsp; <b>38 ms</b> &nbsp;(약 790배)</p>
<div class="pair">
  <div class="box before"><h3>전 — 실습본</h3><pre>SELECT p.prod_cd, p.prod_nm, p.prod_type,
  <span class="hl-bad">(SELECT COUNT(*) FROM account a
     WHERE a.prod_cd = p.prod_cd
       AND a.status = 'NORMAL')</span>   AS 정상계좌수,
  <span class="hl-bad">(SELECT COUNT(DISTINCT a.cust_no) FROM account a
     WHERE a.prod_cd = p.prod_cd)</span>  AS 가입고객수,
  <span class="hl-bad">(SELECT SUM(a.balance) FROM account a
     WHERE a.prod_cd = p.prod_cd
       AND a.status = 'NORMAL')</span>   AS 총잔액
FROM product p
GROUP BY p.prod_cd, p.prod_nm, p.prod_type
<span class="hl-bad">HAVING COUNT(*) &gt; 0</span>
ORDER BY 총잔액 DESC;

<span class="hl-bad">-- account 를 21회 풀스캔 (상품7 x 서브쿼리3)</span></pre></div>
  <div class="box after"><h3>후 — 최적화</h3><pre><span class="hl-good">CREATE INDEX idx_account_prod
    ON account (prod_cd);</span>

SELECT p.prod_cd, p.prod_nm, p.prod_type,
  COUNT(*) <span class="hl-good">FILTER (WHERE a.status='NORMAL')</span>
                                    AS 정상계좌수,
  COUNT(DISTINCT a.cust_no)         AS 가입고객수,
  <span class="hl-good">COALESCE(</span>SUM(a.balance)
    <span class="hl-good">FILTER (WHERE a.status='NORMAL')</span><span class="hl-good">, 0)</span>
                                    AS 총잔액
FROM product p
<span class="hl-good">LEFT JOIN</span> account a ON a.prod_cd = p.prod_cd
GROUP BY p.prod_cd, p.prod_nm, p.prod_type
ORDER BY 총잔액 DESC;</pre></div>
</div>
<table>
  <tr><th>바뀐 것</th><th>전</th><th>후</th><th>왜</th></tr>
  <tr><td>집계 방식</td><td>상관 서브쿼리 3개</td><td><code>LEFT JOIN</code> 1번</td>
      <td>account를 21회 훑던 것을 1회로. 시간의 대부분이 여기 있었다</td></tr>
  <tr><td>조인 종류</td><td>—</td><td><code>LEFT</code></td>
      <td><strong>INNER면 가입 0건 상품(P007 참좋은 파킹통장)이 사라진다.</strong> 업무 요건 위반</td></tr>
  <tr><td>조건별 집계</td><td>서브쿼리마다 WHERE</td><td><code>FILTER (WHERE …)</code></td>
      <td>WHERE로 걸면 세 집계 전부에 적용된다. <code>CASE WHEN</code>도 같은 결과</td></tr>
  <tr><td>NULL 처리</td><td>없음</td><td><code>COALESCE(…, 0)</code></td>
      <td>가입 0건 상품의 SUM은 NULL. 화면엔 0이 나와야 한다</td></tr>
  <tr><td><code>HAVING COUNT(*) &gt; 0</code></td><td>있음</td><td>삭제</td>
      <td>GROUP BY 결과에 0건 그룹은 원래 없다. 무의미하고 오히려 위험</td></tr>
  <tr><td>인덱스</td><td><code>account.prod_cd</code> 없음</td><td><code>idx_account_prod</code></td>
      <td><strong>쿼리만 고치면 절반이다.</strong> 여기서 가장 많이 빠뜨린다</td></tr>
</table>

<h2><em>주의</em>AI 답을 그대로 믿지 마세요</h2>
<div class="check">
<table style="margin-top:0;border:0">
  <tr><th style="border:0;border-bottom:1px solid var(--line)">확인할 것</th>
      <th style="border:0;border-bottom:1px solid var(--line)">왜</th></tr>
  <tr><td style="border:0"><b>날짜 경계</b></td>
      <td style="border:0"><code>&lt; 다음달 1일</code>이어야 하는데 <code>&lt;= 말일</code>로 쓰면 <b>마지막 날이 통째로 빠진다</b></td></tr>
  <tr><td style="border:0"><b>LEFT인지 INNER인지</b></td>
      <td style="border:0">INNER로 바꾸면 가입 0건 상품이 조용히 사라진다</td></tr>
  <tr><td style="border:0"><b>결과 건수</b></td>
      <td style="border:0">문제 2는 상품 7개가 전부 나와야 한다. 6개면 조인이 틀린 것</td></tr>
  <tr><td style="border:0"><b>CREATE INDEX</b></td>
      <td style="border:0">쿼리만 고치고 인덱스를 빼먹는 경우가 가장 많다</td></tr>
</table>
</div>
<p style="margin-top:14px;font-size:14px;color:#374151">
고친 쿼리를 받았으면 <b>"왜 빨라지는지 한 줄로 설명해줘"</b>를 꼭 물어보세요.
설명을 못 하면 그 답은 못 믿습니다.</p>

<p class="foot">SBTI 과정 · SQL 튜닝 실습 · 전부 가상 데이터</p>

</div>
</body>
</html>
'''


def main():
    for rel, body in F.items():
        p = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        io.open(p, 'w', encoding='utf-8').write(body)

    for dp, _, fns in os.walk(ROOT):
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            n = sum(1 for _ in io.open(p, encoding='utf-8'))
            print(f'  {n:>4}줄  {os.path.relpath(p, os.path.dirname(ROOT))}')

    z = ROOT + '.zip'
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for dp, _, fns in os.walk(ROOT):
            for fn in fns:
                if fn == '.DS_Store':
                    continue
                full = os.path.join(dp, fn)
                zf.write(full, os.path.relpath(full, os.path.dirname(ROOT)))
    print(f'\nzip {os.path.getsize(z)/1024:.0f} KB')


if __name__ == '__main__':
    main()
