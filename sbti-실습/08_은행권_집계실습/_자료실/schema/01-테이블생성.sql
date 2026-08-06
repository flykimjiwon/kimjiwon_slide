-- ────────────────────────────────────────────────────────────────────────────
--  ※ 전부 가상입니다. 은행명 · 직원명 · 사번 · 영업점 · 상품명 · 고객번호 ·
--     수치까지 모두 지어낸 값이며 실제 상품·직원·시스템과 아무 관련이 없습니다.
--     교육 실습 전용.
-- ────────────────────────────────────────────────────────────────────────────

-- 가상 은행 「한빛은행」 — 실적/채널 분석계 축약 스키마 (PostgreSQL 기준)

DROP TABLE IF EXISTS page_view_log, app_page, referral, product, employee, branch;

-- ── 영업점 ──────────────────────────────────────────────────────────────
CREATE TABLE branch (
    branch_cd   VARCHAR(6)  PRIMARY KEY,      -- B0101
    branch_nm   VARCHAR(40) NOT NULL,
    region      VARCHAR(20) NOT NULL,         -- 수도권 | 영남 | 호남 | 충청 | 강원
    open_dt     DATE        NOT NULL
);

-- ── 직원 ────────────────────────────────────────────────────────────────
CREATE TABLE employee (
    emp_no      VARCHAR(7)  PRIMARY KEY,      -- 사번 7자리
    emp_nm      VARCHAR(30) NOT NULL,
    branch_cd   VARCHAR(6)  NOT NULL,
    position    VARCHAR(20) NOT NULL,         -- 행원 | 대리 | 과장 | 차장 | 지점장
    hire_dt     DATE        NOT NULL,
    emp_status  VARCHAR(10) NOT NULL          -- 재직 | 휴직 | 퇴직
);
CREATE INDEX idx_employee_branch ON employee (branch_cd);
-- ※ emp_status 에는 인덱스가 없다

-- ── 상품 (통장 + 카드) ──────────────────────────────────────────────────
CREATE TABLE product (
    prod_cd     VARCHAR(8)  PRIMARY KEY,      -- C001 / D001
    prod_nm     VARCHAR(60) NOT NULL,
    prod_type   VARCHAR(10) NOT NULL,         -- CARD | DEPOSIT | SAVING
    card_type   VARCHAR(10),                  -- CHECK | CREDIT | NULL(비카드)
    launch_dt   DATE        NOT NULL,
    sale_yn     CHAR(1)     NOT NULL
);
CREATE INDEX idx_product_type ON product (prod_type);

-- ── 가입권유(추천) 실적 ─────────────────────────────────────────────────
--    한 건 = 직원 1명이 고객 1명에게 상품 1개를 권유해 가입시킨 기록
CREATE TABLE referral (
    ref_id      BIGSERIAL   PRIMARY KEY,
    ref_emp_no  VARCHAR(7)  NOT NULL,         -- 가입권유직원(추천인) 사번
    cust_no     VARCHAR(10) NOT NULL,
    prod_cd     VARCHAR(8)  NOT NULL,
    apply_dt    DATE        NOT NULL,         -- 신청일
    channel     VARCHAR(10) NOT NULL,         -- 창구 | 모바일 | 제휴처
    ref_status  VARCHAR(10) NOT NULL,         -- NORMAL | CANCELLED | REJECTED
    first_amt   NUMERIC(18,0)                 -- 최초 입금액 (카드는 NULL)
);
CREATE INDEX idx_referral_emp_dt ON referral (ref_emp_no, apply_dt);
CREATE INDEX idx_referral_prod   ON referral (prod_cd);

-- ── 앱 페이지 (약 1,000개) ──────────────────────────────────────────────
CREATE TABLE app_page (
    page_id     INTEGER     PRIMARY KEY,
    page_cd     VARCHAR(12) NOT NULL UNIQUE,  -- PG0001
    page_nm     VARCHAR(60) NOT NULL,
    category    VARCHAR(20) NOT NULL,         -- 홈 | 상품 | 이체 | 자산 | 혜택 | 고객센터 | 설정
    depth       SMALLINT    NOT NULL,
    open_dt     DATE        NOT NULL,
    close_dt    DATE                          -- NULL 이면 운영중
);
CREATE INDEX idx_app_page_category ON app_page (category);

-- ── 페이지뷰 로그 ───────────────────────────────────────────────────────
CREATE TABLE page_view_log (
    log_id      BIGSERIAL   PRIMARY KEY,
    page_id     INTEGER     NOT NULL,
    cust_no     VARCHAR(10),                  -- NULL = 비로그인 방문
    session_id  VARCHAR(32) NOT NULL,
    view_at     TIMESTAMP   NOT NULL,
    device      VARCHAR(6)  NOT NULL,         -- AOS | IOS | WEB
    stay_sec    INTEGER     NOT NULL
);
CREATE INDEX idx_pvlog_page_time ON page_view_log (page_id, view_at);
-- ※ view_at 단독 인덱스는 없다
