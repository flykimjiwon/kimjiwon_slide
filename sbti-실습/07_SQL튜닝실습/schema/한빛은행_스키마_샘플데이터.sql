-- ────────────────────────────────────────────────────────────────────────────
--  ※ 전부 가상입니다. 은행명·고객명·계좌번호·상품명·수치 모두 지어낸 값이며
--     실제 상품·고객·시스템과 아무 관련이 없습니다. 교육 실습 전용입니다.
-- ────────────────────────────────────────────────────────────────────────────

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
