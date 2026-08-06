#!/usr/bin/env python3
"""08_은행권_집계실습 — 카드 추천실적 / 앱 페이지뷰 집계 문제 + 정답 + 비교 보고서."""
import io, os, zipfile

ROOT = '/Users/kimjiwon/Desktop/SBTI_PDF_모음_2026-08-05/08_은행권_집계실습'
F = {}

BANNER = """-- ────────────────────────────────────────────────────────────────────────────
--  ※ 전부 가상입니다. 은행명 · 직원명 · 사번 · 영업점 · 상품명 · 고객번호 ·
--     수치까지 모두 지어낸 값이며 실제 상품·직원·시스템과 아무 관련이 없습니다.
--     교육 실습 전용.
-- ────────────────────────────────────────────────────────────────────────────
"""

# ═══════════════════════════════════════════════════ 스키마
F['schema/01-테이블생성.sql'] = BANNER + '''
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
'''

F['schema/02-더미데이터.sql'] = BANNER + '''
-- 더미 데이터 (전부 가상)
--   영업점 8 · 직원 40 · 상품 14 · 추천실적 3,053건 (계획표 기반, 난수 아님)
--   앱 페이지 1,000 · 페이지뷰 로그 120,000건 (결정론적 · 브라우저 실습본과 동일)

-- ── 영업점 ──────────────────────────────────────────────────────────────
INSERT INTO branch (branch_cd, branch_nm, region, open_dt) VALUES
 ('B0101','한빛 본점',        '수도권','1998-03-02'),
 ('B0102','한빛 여의도지점',  '수도권','2004-06-14'),
 ('B0103','한빛 판교지점',    '수도권','2013-09-01'),
 ('B0104','한빛 강릉지점',    '강원',  '2009-04-20'),
 ('B0105','한빛 대전둔산지점','충청',  '2007-11-05'),
 ('B0106','한빛 광주상무지점','호남',  '2011-02-28'),
 ('B0107','한빛 부산서면지점','영남',  '2001-07-16'),
 ('B0108','한빛 창원지점',    '영남',  '2016-05-09');

-- ── 직원 40명 ───────────────────────────────────────────────────────────
INSERT INTO employee (emp_no, emp_nm, branch_cd, position, hire_dt, emp_status) VALUES
 ('1000001','김하늘','B0101','과장','2013-01-07','재직'),
 ('1000002','이바다','B0101','대리','2017-03-13','재직'),
 ('1000003','박구름','B0101','행원','2022-09-05','재직'),
 ('1000004','최나무','B0101','차장','2008-11-24','재직'),
 ('1000005','정바람','B0102','행원','2021-06-14','재직'),
 ('1000006','강별',  'B0102','대리','2016-08-01','재직'),
 ('1000007','윤노을','B0102','과장','2012-04-16','재직'),
 ('1000008','서한결','B0102','행원','2023-02-20','재직'),
 ('1000009','한소망','B0103','대리','2018-05-28','재직'),
 ('1000010','오늘봄','B0103','행원','2024-01-08','재직'),
 ('1000011','신여울','B0103','과장','2011-10-17','재직'),
 ('1000012','문가온','B0103','행원','2022-03-21','휴직'),
 ('1000013','임소울','B0104','대리','2015-07-06','재직'),
 ('1000014','조미르','B0104','행원','2023-08-14','재직'),
 ('1000015','배아람','B0104','지점장','2003-02-10','재직'),
 ('1000016','권도담','B0105','과장','2010-12-06','재직'),
 ('1000017','류지음','B0105','행원','2021-11-29','재직'),
 ('1000018','남해린','B0105','대리','2017-09-11','퇴직'),
 ('1000019','도이든','B0106','행원','2022-05-02','재직'),
 ('1000020','명가람','B0106','과장','2014-03-24','재직'),
 ('1000021','반슬기','B0106','대리','2019-01-14','재직'),
 ('1000022','설다온','B0107','행원','2023-04-03','재직'),
 ('1000023','양하람','B0107','차장','2006-08-21','재직'),
 ('1000024','엄나래','B0107','대리','2018-10-15','재직'),
 ('1000025','우겨레','B0107','행원','2024-02-26','재직'),
 ('1000026','장미소','B0108','과장','2012-07-09','재직'),
 ('1000027','전누리','B0108','행원','2021-04-19','재직'),
 ('1000028','차보람','B0108','대리','2016-11-07','퇴직'),
 ('1000029','추한별','B0101','행원','2023-06-12','재직'),
 ('1000030','표새롬','B0102','행원','2024-03-04','재직'),
 ('1000031','하늘찬','B0103','대리','2019-08-26','재직'),
 ('1000032','허가람','B0104','행원','2022-12-05','재직'),
 ('1000033','홍이레','B0105','행원','2023-09-18','재직'),
 ('1000034','황단비','B0106','대리','2018-02-12','재직'),
 ('1000035','고운결','B0107','행원','2024-05-20','재직'),
 ('1000036','구름솔','B0108','행원','2023-01-16','재직'),
 ('1000037','노을빛','B0101','대리','2017-05-22','재직'),
 ('1000038','다솔찬','B0102','과장','2013-09-30','재직'),
 ('1000039','라온제','B0103','행원','2022-08-08','휴직'),
 ('1000040','마루한','B0104','대리','2019-12-02','재직');

-- ── 상품 14개 (카드 8 · 수신 6) ─────────────────────────────────────────
INSERT INTO product (prod_cd, prod_nm, prod_type, card_type, launch_dt, sale_yn) VALUES
 ('C001','나라지킴이 체크카드',   'CARD','CHECK', '2019-03-04','Y'),
 ('C002','새내기 첫걸음 체크카드','CARD','CHECK', '2021-02-15','Y'),
 ('C003','한빛 실속 신용카드',    'CARD','CREDIT','2018-06-01','Y'),
 ('C004','드림포인트 신용카드',   'CARD','CREDIT','2020-09-10','Y'),
 ('C005','실버케어 체크카드',     'CARD','CHECK', '2022-04-25','Y'),
 ('C006','그린모빌리티 신용카드', 'CARD','CREDIT','2023-05-30','Y'),
 ('C007','한빛 트래블 체크카드',  'CARD','CHECK', '2024-01-11','Y'),
 ('C008','옛길 클래식 신용카드',  'CARD','CREDIT','2012-08-20','N'),
 ('D001','행복드림 자유적금',     'SAVING',  NULL,'2017-05-02','Y'),
 ('D002','든든플러스 정기예금',   'DEPOSIT', NULL,'2015-01-19','Y'),
 ('D003','새싹 청년우대적금',     'SAVING',  NULL,'2021-07-07','Y'),
 ('D004','미래설계 연금저축',     'SAVING',  NULL,'2019-11-13','Y'),
 ('D005','슬기로운 주택청약',     'SAVING',  NULL,'2010-03-08','Y'),
 ('D006','참좋은 파킹통장',       'DEPOSIT', NULL,'2023-02-01','N');

-- ── 가입권유(추천) 실적 ─────────────────────────────────────────────────
--    난수가 아니라 계획표로 만든다. 이 표가 곧 정답의 근거다.
--      · 카드 NORMAL 52건 동점 2명            → 공동 1위
--      · 퇴직자 남해린(1000018)에게 50건      → 재직 필터를 빠뜨리면 3위에 끼어든다
--      · 휴직자 문가온(1000012)에게 28건      → 역시 제외 대상
--      · 카드 NORMAL 33건 동점 3명            → 공동 10위 (정답은 12행)
--      · 카드 6건 이상인 직원은 추천고객수 = (카드건수 - 5) → 건수 ≠ 고객수
--      · 기간 밖(2025 하반기) 건수는 실적이 낮은 직원일수록 많이 넣었다
--        → 날짜 필터를 빠뜨리면 전원 60건으로 뭉개져 순위가 무의미해진다
CREATE TEMP TABLE ref_plan (
    emp_no     VARCHAR(7),
    card_cnt   INTEGER,      -- 카드 NORMAL (2026 상반기)
    cancel_cnt INTEGER,      -- 카드 CANCELLED (2026 상반기)
    dep_cnt    INTEGER       -- 수신(비카드) NORMAL — 상품 필터 확인용 노이즈
);
INSERT INTO ref_plan VALUES
 ('1000001',52,6,30), ('1000023',52,2,22), ('1000018',50,4,18), ('1000007',47,5,25),
 ('1000016',45,3,19), ('1000004',43,7,28), ('1000011',41,2,16), ('1000020',39,4,21),
 ('1000026',37,1,14), ('1000009',35,3,17), ('1000013',33,2,12), ('1000021',33,5,20),
 ('1000034',33,0,11), ('1000006',31,3,15), ('1000024',29,2,13), ('1000031',27,1,18),
 ('1000002',26,4,24), ('1000037',24,2, 9), ('1000038',23,3,16), ('1000015',21,1, 8),
 ('1000040',20,2,12), ('1000005',18,3,10), ('1000017',17,1, 7), ('1000019',16,2,11),
 ('1000027',15,1, 9), ('1000003',14,2, 6), ('1000008',13,1, 8), ('1000010',12,0, 5),
 ('1000014',11,1, 7), ('1000022',10,2, 4), ('1000025', 9,0, 6), ('1000029', 8,1, 3),
 ('1000030', 7,0, 5), ('1000032', 6,1, 4), ('1000033', 5,0, 3), ('1000035', 4,1, 2),
 ('1000036', 3,0, 2), ('1000028',19,2,10), ('1000012',28,3,14), ('1000039', 9,1, 5);

-- 카드 NORMAL (2026 상반기) — 고객을 5명 중복시켜 건수 ≠ 고객수 를 만든다
INSERT INTO referral (ref_emp_no, cust_no, prod_cd, apply_dt, channel, ref_status, first_amt)
SELECT p.emp_no,
       'C' || LPAD((((p.emp_no::bigint % 1000) * 1000)
                    + ((s - 1) % GREATEST(p.card_cnt - 5, 1)) + 1)::text, 9, '0'),
       'C00' || (1 + (s % 8)),
       DATE '2026-01-01' + ((s * 11) % 180),
       (ARRAY['창구','모바일','제휴처'])[1 + (s % 3)],
       'NORMAL', NULL
FROM ref_plan p CROSS JOIN generate_series(1, 60) s
WHERE s <= p.card_cnt;

-- 카드 CANCELLED (2026 상반기)
INSERT INTO referral (ref_emp_no, cust_no, prod_cd, apply_dt, channel, ref_status, first_amt)
SELECT p.emp_no,
       'C' || LPAD((((p.emp_no::bigint % 1000) * 1000) + 900 + s)::text, 9, '0'),
       'C00' || (1 + (s % 8)),
       DATE '2026-01-01' + ((s * 29) % 180),
       '창구', 'CANCELLED', NULL
FROM ref_plan p CROSS JOIN generate_series(1, 10) s
WHERE s <= p.cancel_cnt;

-- 카드 REJECTED — 실적에도 취소에도 들어가면 안 되는 노이즈 (직원당 2건)
INSERT INTO referral (ref_emp_no, cust_no, prod_cd, apply_dt, channel, ref_status, first_amt)
SELECT p.emp_no,
       'C' || LPAD((((p.emp_no::bigint % 1000) * 1000) + 950 + s)::text, 9, '0'),
       'C00' || (1 + (s % 8)),
       DATE '2026-02-01' + (s * 13),
       '모바일', 'REJECTED', NULL
FROM ref_plan p CROSS JOIN generate_series(1, 2) s;

-- 수신(비카드) NORMAL — 카드만 세야 한다는 조건 확인용
INSERT INTO referral (ref_emp_no, cust_no, prod_cd, apply_dt, channel, ref_status, first_amt)
SELECT p.emp_no,
       'C' || LPAD((((p.emp_no::bigint % 1000) * 1000) + 700 + s)::text, 9, '0'),
       'D00' || (1 + (s % 6)),
       DATE '2026-01-01' + ((s * 7) % 180),
       (ARRAY['창구','모바일'])[1 + (s % 2)],
       'NORMAL', 100000 + (s % 40) * 50000
FROM ref_plan p CROSS JOIN generate_series(1, 40) s
WHERE s <= p.dep_cnt;

-- 기간 밖(2025 하반기) 카드 NORMAL — 실적 낮은 직원일수록 많이
INSERT INTO referral (ref_emp_no, cust_no, prod_cd, apply_dt, channel, ref_status, first_amt)
SELECT p.emp_no,
       'C' || LPAD((((p.emp_no::bigint % 1000) * 1000) + 600 + s)::text, 9, '0'),
       'C00' || (1 + (s % 8)),
       DATE '2025-07-01' + ((s * 3) % 180),
       '창구', 'NORMAL', NULL
FROM ref_plan p CROSS JOIN generate_series(1, 60) s
WHERE s <= GREATEST(60 - p.card_cnt, 0);

-- ── 앱 페이지 1,000개 ───────────────────────────────────────────────────
--    앞 20개는 실제 화면처럼 이름을 붙이고, 나머지는 자동 생성한다.
INSERT INTO app_page (page_id, page_cd, page_nm, category, depth, open_dt, close_dt) VALUES
 (1,  'PG0001','홈',                    '홈',     1,'2019-01-01',NULL),
 (2,  'PG0002','전체계좌조회',          '자산',   2,'2019-01-01',NULL),
 (3,  'PG0003','이체하기',              '이체',   2,'2019-01-01',NULL),
 (4,  'PG0004','자주쓰는 이체',         '이체',   3,'2019-06-01',NULL),
 (5,  'PG0005','프리미어 라운지',       '혜택',   2,'2021-03-01',NULL),
 (6,  'PG0006','상품몰 메인',           '상품',   2,'2019-01-01',NULL),
 (7,  'PG0007','카드상품 목록',         '상품',   3,'2019-01-01',NULL),
 (8,  'PG0008','예적금 상품 목록',      '상품',   3,'2019-01-01',NULL),
 (9,  'PG0009','나라지킴이 체크카드 상세','상품',  4,'2019-03-04',NULL),
 (10, 'PG0010','새내기 첫걸음 체크카드 상세','상품',4,'2021-02-15',NULL),
 (11, 'PG0011','내 자산 리포트',        '자산',   2,'2020-05-01',NULL),
 (12, 'PG0012','소비 분석',             '자산',   3,'2020-05-01',NULL),
 (13, 'PG0013','포인트 혜택',           '혜택',   2,'2019-01-01',NULL),
 (14, 'PG0014','이벤트 목록',           '혜택',   3,'2019-01-01',NULL),
 (15, 'PG0015','고객센터 메인',         '고객센터',2,'2019-01-01',NULL),
 (16, 'PG0016','자주 묻는 질문',        '고객센터',3,'2019-01-01',NULL),
 (17, 'PG0017','알림 설정',             '설정',   2,'2019-01-01',NULL),
 (18, 'PG0018','간편비밀번호 변경',     '설정',   3,'2019-01-01',NULL),
 (19, 'PG0019','구 이벤트 페이지',      '혜택',   3,'2019-01-01','2025-12-31'),  -- 폐쇄
 (20, 'PG0020','구 상품몰',             '상품',   2,'2019-01-01','2024-06-30');  -- 폐쇄

INSERT INTO app_page (page_id, page_cd, page_nm, category, depth, open_dt, close_dt)
SELECT
    20 + g,
    'PG' || LPAD((20 + g)::text, 4, '0'),
    (ARRAY['상품 상세','거래 내역','약관 안내','신청 결과','인증 화면',
           '혜택 상세','설정 상세','안내 팝업','조회 결과','가입 단계'])[1 + (g % 10)]
      || ' ' || (20 + g),
    (ARRAY['홈','상품','이체','자산','혜택','고객센터','설정'])[1 + (g % 7)],
    2 + (g % 3),
    DATE '2019-01-01' + (g % 2200),
    CASE WHEN g % 97 = 0 THEN DATE '2025-06-30' ELSE NULL END   -- 약 10개가 폐쇄 상태
FROM generate_series(1, 980) AS g;

-- ── 페이지뷰 로그 120,000건 (2026-07-01 ~ 2026-07-31) ──────────────────
--    난수를 쓰지 않는다. 필드마다 서로 다른 승수의 선형합동식을 써서
--    (승수가 같고 덧셈상수만 다르면 필드끼리 완전히 상관돼 버린다)
--    브라우저 실습본(SQL실행기.html)과 완전히 같은 값을 만든다.
--    트래픽은 앞쪽 620개 페이지에만 발생시킨다. 나머지는 신규·비활성 페이지로 두어
--    조회가 한 건도 없게 만든다 → 문제 2의 핵심 재료(PV=0 페이지)다.
INSERT INTO page_view_log (page_id, cust_no, session_id, view_at, device, stay_sec)
SELECT
    -- 세션의 1/3 은 한 페이지만 계속 보는 세션이다 (세션수 < PV 가 되도록)
    1 + FLOOR(POWER((((CASE WHEN g % 3 = 0 THEN 1 + (g % 27000) ELSE g END)::bigint
                      * 2654435761 + 7) % 2147483647) / 2147483647.0, 2.6) * 620)::int,
    CASE WHEN ((g::bigint * 1103515245 + 12345)            % 2147483647) % 100 < 18
         THEN NULL
         ELSE 'C' || LPAD((1 + ((g::bigint * 1013904223 + 1) % 2147483647) % 4000)::text, 9, '0')
    END,
    'S' || LPAD((1 + ((g::bigint * 22695477 + 1)           % 2147483647) % 27000)::text, 8, '0'),
    TIMESTAMP '2026-07-01 00:00:00'
      + ((((g::bigint * 214013 + 2531011)                  % 2147483647) % 44640) * INTERVAL '1 minute'),
    (ARRAY['AOS','IOS','WEB'])[1 + ((g::bigint * 69069 + 5) % 2147483647) % 3],
    (3 + ((g::bigint * 1664525 + 1013904223)               % 2147483647) % 300)::int
FROM generate_series(1, 120000) AS g;

ANALYZE;
'''

# ═══════════════════════════════════════════════════ 문제 1
F['문제/문제1_카드추천실적_상위10명.sql'] = BANNER + '''
-- ════════════════════════════════════════════════════════════════════════
--  [문제 1]  2026년 상반기 카드 가입권유 실적 상위 10명        ★★★
-- ════════════════════════════════════════════════════════════════════════
--
--  요청 (영업기획부)
--    "2026년 상반기 카드 추천 실적 상위 10명 뽑아주세요.
--     이름이랑 지점, 몇 건인지, 몇 명한테 팔았는지, 취소는 얼마나 났는지까지요."
--
--  정확한 요건
--    1. 기간      : 2026-01-01 ~ 2026-06-30  (신청일 apply_dt 기준)
--    2. 대상 상품 : 카드만 (product.prod_type = 'CARD')
--    3. 실적 인정 : ref_status = 'NORMAL' 인 건만 센다
--                   ('CANCELLED', 'REJECTED' 는 실적에서 제외)
--    4. 대상 직원 : emp_status = '재직' 인 직원만
--    5. 순위      : ★ 추천건수 기준으로만 매긴다 ★
--                   추천건수가 같으면 같은 순위다 (공동 1위, 공동 10위가 생긴다)
--    6. 상위 10명 : ★ 순위 10 이내를 전부 출력한다 ★
--                   10위가 동점이면 10명을 넘겨도 전부 나와야 한다
--    7. 출력 정렬  : 순위 → 추천고객수 내림차순 → 사번 오름차순
--
--  출력 컬럼
--    순위 · 사번 · 직원명 · 영업점명 · 직급 · 추천건수 · 추천고객수 · 취소건수 · 취소율(%)
--
--    · 추천건수   : NORMAL 건수
--    · 추천고객수 : NORMAL 건의 서로 다른 고객 수 (한 고객이 카드 2장이면 1명)
--    · 취소건수   : 같은 기간·같은 직원의 CANCELLED 건수
--    · 취소율     : 취소건수 / (추천건수 + 취소건수) * 100, 소수점 1자리
--
--  참고 인덱스
--    referral : idx_referral_emp_dt (ref_emp_no, apply_dt), idx_referral_prod (prod_cd)
--    employee : PK(emp_no), idx_employee_branch (branch_cd)
--    product  : PK(prod_cd), idx_product_type (prod_type)
--
-- ════════════════════════════════════════════════════════════════════════


-- ▼ 여기에 쿼리를 작성하세요.
--   다 쓰고 나면 정답/정답1_카드추천실적_상위10명.sql 과 비교합니다.









-- ────────────────────────────────────────────────────────────────────────
--  스스로 점검할 질문
--    1. "상위 10명" 을 LIMIT 10 으로 쓰면 동점자는 어떻게 되는가?
--    2. 추천건수와 추천고객수는 왜 다른가? 어떤 함수를 써야 하는가?
--    3. 취소건수는 실적에서 제외한다면서 왜 또 세어야 하는가?
--       WHERE ref_status='NORMAL' 로 걸어버리면 취소건수를 셀 수 있는가?
--    4. 퇴직자를 거르는 조건은 순위를 매기기 전에 걸어야 하는가, 후에 걸어야 하는가?
--    5. 취소율 분모가 0이 되는 경우는 없는가?
-- ────────────────────────────────────────────────────────────────────────
'''

# ═══════════════════════════════════════════════════ 정답 1
F['정답/정답1_카드추천실적_상위10명.sql'] = BANNER + '''
-- ════════════════════════════════════════════════════════════════════════
--  [문제 1 정답]  카드 가입권유 실적 상위 10명
-- ════════════════════════════════════════════════════════════════════════

WITH card_ref AS (
    -- 기간·카드·재직 조건을 한 번에 걸고 referral 을 딱 한 번만 읽는다.
    -- ref_status 는 여기서 거르지 않는다. 취소건수도 세야 하기 때문이다.
    SELECT r.ref_emp_no,
           r.cust_no,
           r.ref_status
    FROM referral r
    JOIN product  p ON p.prod_cd = r.prod_cd
    JOIN employee e ON e.emp_no  = r.ref_emp_no
    WHERE p.prod_type = 'CARD'
      AND e.emp_status = '재직'                          -- 순위 매기기 "전"에 제외
      AND r.apply_dt >= DATE '2026-01-01'
      AND r.apply_dt <  DATE '2026-07-01'                -- < 7월 1일  (<= 6월 30일 아님)
),
agg AS (
    SELECT ref_emp_no,
           COUNT(*)          FILTER (WHERE ref_status = 'NORMAL')    AS 추천건수,
           COUNT(DISTINCT cust_no) FILTER (WHERE ref_status = 'NORMAL') AS 추천고객수,
           COUNT(*)          FILTER (WHERE ref_status = 'CANCELLED') AS 취소건수
    FROM card_ref
    GROUP BY ref_emp_no
),
ranked AS (
    SELECT a.*,
           RANK() OVER (ORDER BY a.추천건수 DESC) AS 순위   -- 순위는 추천건수 기준만
    FROM agg a
    WHERE a.추천건수 > 0
)
SELECT r.순위,
       r.ref_emp_no                          AS 사번,
       e.emp_nm                              AS 직원명,
       b.branch_nm                           AS 영업점명,
       e.position                            AS 직급,
       r.추천건수,
       r.추천고객수,
       r.취소건수,
       ROUND( r.취소건수 * 100.0
              / NULLIF(r.추천건수 + r.취소건수, 0), 1)  AS "취소율(%)"
FROM ranked r
JOIN employee e ON e.emp_no    = r.ref_emp_no
JOIN branch   b ON b.branch_cd = e.branch_cd
WHERE r.순위 <= 10
ORDER BY r.순위, r.추천고객수 DESC, r.ref_emp_no;


-- ════════════════════════════════════════════════════════════════════════
--  왜 이렇게 썼나 — 함정 5개
--
--  ① 동점 처리          RANK() OVER (...) 로 순위를 매기고 순위 <= 10 으로 자른다.
--                       LIMIT 10 을 쓰면 10위 동점자 중 일부가 임의로 잘린다.
--                       "상위 10명" 이라는 말만 보고 LIMIT 을 쓰는 것이 가장 흔한 오답.
--                       (동점자를 포함해 10명을 넘겨도 되는지는 요건 6에 명시돼 있다)
--
--  ② 건수 vs 고객수     COUNT(*) 와 COUNT(DISTINCT cust_no) 는 다르다.
--                       한 고객에게 카드 2장을 팔면 건수 2 · 고객수 1.
--
--  ③ 취소건수를 세는 법  WHERE ref_status = 'NORMAL' 로 걸어버리면 취소 건이
--                       사라져서 셀 수가 없다. 조건을 WHERE 가 아니라
--                       FILTER (WHERE ...) 로 옮겨 한 번의 스캔으로 둘 다 센다.
--                       (FILTER 미지원 DBMS 는 SUM(CASE WHEN ... THEN 1 ELSE 0 END))
--
--  ④ 퇴직자 제외 시점    순위를 매긴 뒤에 거르면 1~10위 사이에 구멍이 생긴다.
--                       (예: 3위가 퇴직자면 결과가 9명이 된다)
--                       반드시 집계 전에 걸러야 한다.
--
--  ⑤ 날짜 경계          apply_dt 는 DATE 라 <= '2026-06-30' 도 결과는 같다.
--                       하지만 TIMESTAMP 로 바뀌는 순간 6/30 하루가 통째로 빠진다.
--                       처음부터 < 다음달 1일 로 쓰는 습관이 안전하다.
--
--  ⑥ 0 나눗셈           취소율 분모가 0이 될 수 있으므로 NULLIF 로 막는다.
--
-- ════════════════════════════════════════════════════════════════════════

-- ════════════════════════════════════════════════════════════════════════
--  검증된 실행 결과  (PostgreSQL 에서 실제로 돌려 확인함)
--
--    결과 12행.  ← 10명이 아니다. 공동 10위가 3명이라 12행이 정답이다.
--
--      순위  사번      직원명  영업점            건수  고객수  취소  취소율
--       1    1000001   김하늘  한빛 본점          52     47      6   10.3
--       1    1000023   양하람  한빛 부산서면지점  52     47      2    3.7
--       3    1000007   윤노을  한빛 여의도지점    47     42      5    9.6
--       4    1000016   권도담  한빛 대전둔산지점  45     40      3    6.3
--       5    1000004   최나무  한빛 본점          43     38      7   14.0
--       6    1000011   신여울  한빛 판교지점      41     36      2    4.7
--       7    1000020   명가람  한빛 광주상무지점  39     34      4    9.3
--       8    1000026   장미소  한빛 창원지점      37     32      1    2.6
--       9    1000009   한소망  한빛 판교지점      35     30      3    7.9
--      10    1000013   임소울  한빛 강릉지점      33     28      2    5.7
--      10    1000021   반슬기  한빛 광주상무지점  33     28      5   13.2
--      10    1000034   황단비  한빛 광주상무지점  33     28      0    0.0
--
--  틀렸을 때 나오는 결과 (채점용)
--    · LIMIT 10 사용        → 10행. 공동 10위 3명 중 1명이 조용히 잘린다
--    · 재직 필터 누락       → 3위에 퇴직자 「남해린」(1000018, 50건)이 끼어든다
--    · 날짜 필터 누락       → 전원 60건으로 뭉개져 순위가 1개 값이 된다
--    · WHERE ref_status 사용 → 취소건수가 전부 0 이 된다
--    · COUNT(*) 로 고객수    → 고객수가 건수와 똑같아진다 (정답은 5 작다)
-- ════════════════════════════════════════════════════════════════════════
'''

# ═══════════════════════════════════════════════════ 문제 2
F['문제/문제2_앱페이지뷰_집계.sql'] = BANNER + '''
-- ════════════════════════════════════════════════════════════════════════
--  [문제 2]  2026년 7월 앱 페이지별 조회수 · 방문자수                ★★★
-- ════════════════════════════════════════════════════════════════════════
--
--  요청 (디지털채널부)
--    "7월 페이지별로 조회수랑 방문자수 좀 뽑아주세요.
--     프리미어 라운지랑 상품 페이지들이 궁금해요. 아무도 안 본 페이지도 봐야 해요."
--
--  정확한 요건
--    1. 기간      : 2026-07-01 00:00 ~ 2026-07-31 23:59:59.999  (view_at 기준)
--    2. 대상 페이지: 폐쇄되지 않은 페이지
--                   (close_dt IS NULL 이거나 close_dt >= 2026-07-01)
--    3. 지표
--         PV(조회수)     : 로그 건수
--         UV(방문자수)   : 서로 다른 고객 수. 비로그인(cust_no IS NULL)은 제외
--         세션수         : 서로 다른 session_id 수 (비로그인 포함)
--         평균체류(초)   : stay_sec 평균, 소수점 1자리
--    4. ★ 조회가 0건인 페이지도 결과에 나와야 한다. PV·UV·세션수는 0 으로 표시 ★
--    5. 정렬      : PV 내림차순, 같으면 page_id 오름차순
--    6. 상위 20개 페이지
--
--  출력 컬럼
--    페이지코드 · 페이지명 · 카테고리 · PV · UV · 세션수 · 평균체류초
--
--  참고 인덱스
--    page_view_log : PK(log_id), idx_pvlog_page_time (page_id, view_at)
--                    ※ view_at 단독 인덱스는 없다
--    app_page      : PK(page_id), UNIQUE(page_cd), idx_app_page_category (category)
--
--  데이터 규모
--    app_page 1,000행 · page_view_log 120,000행
--
-- ════════════════════════════════════════════════════════════════════════


-- ▼ 여기에 쿼리를 작성하세요.









-- ────────────────────────────────────────────────────────────────────────
--  스스로 점검할 질문
--    1. "조회 0건 페이지도 나와야 한다" 면 어떤 조인을 써야 하는가?
--    2. 그 조인을 쓴 상태에서 기간 조건을 WHERE 에 두면 무슨 일이 일어나는가?
--       (0건 페이지가 그대로 남아 있는가?)
--    3. LEFT JOIN 상태에서 COUNT(*) 는 매칭 0건인 페이지에 대해 얼마를 돌려주는가?
--    4. UV 를 COUNT(DISTINCT cust_no) 로 세면 비로그인 방문은 어떻게 처리되는가?
--       요건과 맞는가?
--    5. 평균체류시간은 로그가 없는 페이지에서 무엇이 되는가? 화면에 어떻게 나가야 하는가?
-- ────────────────────────────────────────────────────────────────────────
'''

# ═══════════════════════════════════════════════════ 정답 2
F['정답/정답2_앱페이지뷰_집계.sql'] = BANNER + '''
-- ════════════════════════════════════════════════════════════════════════
--  [문제 2 정답]  앱 페이지별 조회수 · 방문자수
-- ════════════════════════════════════════════════════════════════════════

SELECT p.page_cd                                   AS 페이지코드,
       p.page_nm                                   AS 페이지명,
       p.category                                  AS 카테고리,
       COUNT(l.log_id)                             AS "PV",
       COUNT(DISTINCT l.cust_no)                   AS "UV",
       COUNT(DISTINCT l.session_id)                AS 세션수,
       COALESCE(ROUND(AVG(l.stay_sec)::numeric, 1), 0) AS 평균체류초
FROM app_page p
LEFT JOIN page_view_log l
       ON l.page_id  = p.page_id
      AND l.view_at >= TIMESTAMP '2026-07-01 00:00:00'
      AND l.view_at <  TIMESTAMP '2026-08-01 00:00:00'   -- ★ 기간 조건은 ON 절에
WHERE p.close_dt IS NULL
   OR p.close_dt >= DATE '2026-07-01'
GROUP BY p.page_cd, p.page_nm, p.category, p.page_id
ORDER BY "PV" DESC, p.page_id
LIMIT 20;


-- ════════════════════════════════════════════════════════════════════════
--  왜 이렇게 썼나 — 함정 5개
--
--  ① 기간 조건을 ON 에 둔다     ← 이 문제의 핵심
--     WHERE l.view_at >= ... 로 쓰면 로그가 없는 페이지는 view_at 이 NULL 이라
--     조건에서 탈락한다. 결과적으로 LEFT JOIN 이 INNER JOIN 처럼 동작해
--     "조회 0건 페이지" 가 통째로 사라진다.
--     LEFT JOIN 의 오른쪽 테이블 조건은 ON 절에 둬야 한다.
--
--  ② COUNT(*) 가 아니라 COUNT(l.log_id)
--     LEFT JOIN 에서 매칭이 없으면 오른쪽 컬럼이 NULL 인 행이 1개 생긴다.
--     COUNT(*) 는 그 행을 세어 1 을 돌려준다. 조회 0건인데 PV=1 이 된다.
--     COUNT(컬럼) 은 NULL 을 세지 않으므로 0 이 나온다.
--
--  ③ UV 는 COUNT(DISTINCT cust_no)
--     COUNT(DISTINCT) 는 NULL 을 세지 않는다. 비로그인 방문이 자동으로 빠진다.
--     이번 요건은 "비로그인 제외" 이므로 이 동작이 맞다.
--     만약 비로그인도 1명으로 세야 한다면 요건이 달라지고 쿼리도 달라진다.
--     → 세션 기준이면 COUNT(DISTINCT session_id) 를 UV 로 쓴다.
--
--  ④ 폐쇄 페이지 조건은 WHERE 에
--     app_page 는 왼쪽 테이블이므로 WHERE 에 두는 것이 맞다.
--     ON 절에 넣으면 폐쇄 페이지가 0건으로 남아버린다.
--
--  ⑤ 평균체류시간 NULL
--     로그가 없으면 AVG 는 NULL 이다. 화면에 빈칸이 아니라 0 이 나가야 하므로
--     COALESCE 로 감싼다.
--
--  검증 방법
--    · 결과에 PV=0 인 페이지가 섞여 나오는지 확인한다. 전부 PV>0 이면 ① 을 틀린 것이다.
--    · LIMIT 을 빼고 COUNT(*) 를 세면 운영중 페이지 수 988 과 같아야 한다.
--      더 적으면 조인이나 조건이 잘못됐다.
--
-- ════════════════════════════════════════════════════════════════════════

-- ════════════════════════════════════════════════════════════════════════
--  검증된 실행 결과  (PostgreSQL 에서 실제로 돌려 확인함)
--
--    LIMIT 20 을 빼면 988행 (운영중 페이지 수).  그중 376행이 PV=0 이다.
--
--      페이지코드  페이지명          카테고리   PV      UV     세션수   평균체류초
--      PG0001      홈                홈         33,793  3,999  28,084   152.9
--      PG0002      전체계좌조회      자산       10,204  3,499   9,628   151.4
--      PG0003      이체하기          이체        7,440  3,116   7,129   151.8
--      PG0004      자주쓰는 이체     이체        6,094  2,852   5,894   153.5
--      PG0005      프리미어 라운지   혜택        5,170  2,608   5,040   152.0
--
--  틀렸을 때 나오는 결과 (채점용)
--    · 기간조건을 WHERE 에 → 988행이 612행으로 줄어든다. 376개 페이지가 사라진다.
--                            ★ 에러도 안 나고 상위 20개는 정답과 똑같아서
--                              LIMIT 20 만 보면 절대 못 잡는다 ★
--    · COUNT(*) 사용        → PV=0 인 페이지 376개가 전부 PV=1 로 나온다
--    · INNER JOIN 사용      → 기간조건을 WHERE 에 둔 것과 같은 결과
--    · 폐쇄 페이지 조건 누락 → 1000행이 된다 (988 + 폐쇄 12)
--
--  자가 검증법
--    LIMIT 20 을 지우고 SELECT COUNT(*) 로 감싸 보세요. 988 이 나와야 합니다.
-- ════════════════════════════════════════════════════════════════════════



-- ▼ 참고 : 카테고리별 소계까지 함께 보고 싶을 때
--
-- SELECT COALESCE(p.category, '── 전체 ──') AS 카테고리,
--        COUNT(l.log_id) AS "PV",
--        COUNT(DISTINCT l.cust_no) AS "UV"
-- FROM app_page p
-- LEFT JOIN page_view_log l
--        ON l.page_id = p.page_id
--       AND l.view_at >= TIMESTAMP '2026-07-01 00:00:00'
--       AND l.view_at <  TIMESTAMP '2026-08-01 00:00:00'
-- WHERE p.close_dt IS NULL OR p.close_dt >= DATE '2026-07-01'
-- GROUP BY ROLLUP (p.category)
-- ORDER BY "PV" DESC;
'''

# ═══════════════════════════════════════════════════ 프롬프트
F['예시프롬프트.md'] = '''# 예시 프롬프트 — 그대로 복사해서 쓰세요

같은 문제를 **Claude** 와 **Qwen3.6-35B(온프렘)** 에 각각 넣고 결과를 비교합니다.
프롬프트는 **똑같이** 넣어야 비교가 됩니다.

---

## A. 한 번에 물어보기 (기본형)

두 모델에 똑같이 넣습니다. 이게 기본 비교선입니다.

```
아래 요건대로 PostgreSQL 쿼리를 작성해줘.

[테이블]
referral(ref_id, ref_emp_no, cust_no, prod_cd, apply_dt, channel, ref_status, first_amt)
employee(emp_no, emp_nm, branch_cd, position, hire_dt, emp_status)
branch(branch_cd, branch_nm, region, open_dt)
product(prod_cd, prod_nm, prod_type, card_type, launch_dt, sale_yn)

[요건]
- 2026-01-01 ~ 2026-06-30 신청분
- 카드 상품만 (product.prod_type = 'CARD')
- 실적은 ref_status='NORMAL' 인 건만 인정
- 재직중인 직원만 (employee.emp_status = '재직')
- 순위는 추천건수 기준으로만 매긴다 (같으면 공동 순위)
- 순위 10 이내를 전부 출력. 10위가 동점이면 10명을 넘겨도 전부 나와야 함
- 출력 정렬: 순위, 추천고객수 내림차순, 사번 오름차순
- 출력: 순위, 사번, 직원명, 영업점명, 직급, 추천건수, 추천고객수, 취소건수, 취소율(%)
  * 추천고객수 = 서로 다른 고객 수
  * 취소건수 = 같은 기간·같은 직원의 ref_status='CANCELLED' 건수
  * 취소율 = 취소건수 / (추천건수+취소건수) * 100, 소수점 1자리
```

```
아래 요건대로 PostgreSQL 쿼리를 작성해줘.

[테이블]
app_page(page_id, page_cd, page_nm, category, depth, open_dt, close_dt)
page_view_log(log_id, page_id, cust_no, session_id, view_at, device, stay_sec)

[요건]
- 2026년 7월 한 달간의 page_view_log 기준
- 폐쇄 페이지 제외 (close_dt IS NULL 이거나 close_dt >= 2026-07-01)
- PV = 로그 건수, UV = 서로 다른 고객 수(비로그인 cust_no IS NULL 은 제외),
  세션수 = 서로 다른 session_id 수, 평균체류초 = stay_sec 평균(소수점 1자리)
- 조회가 0건인 페이지도 0으로 표시되어야 함
- PV 내림차순, 같으면 page_id 오름차순, 상위 20개
- 출력: 페이지코드, 페이지명, 카테고리, PV, UV, 세션수, 평균체류초
```

---

## B. 나눠서 물어보기 (온프렘 모델용)

35B 모델이 A 에서 틀렸다면, 아래처럼 쪼개서 다시 시켜보세요.
**「한 번에 못 하던 것이 나눠주면 되는가」** 를 보는 것이 이 실습의 관전 포인트입니다.

**1단계 — 요건 확인부터**

```
이 요건에서 "상위 10명" 인데 "10위와 동점이면 함께 나와야 한다" 고 되어 있어.
LIMIT 10 으로 처리해도 되는지 알려줘. 안 된다면 어떤 함수를 써야 하는지도.
```

**2단계 — 부분 쿼리**

```
referral 을 한 번만 읽으면서 NORMAL 건수와 CANCELLED 건수를 동시에 세는
집계 쿼리를 만들어줘. WHERE 로 상태를 걸면 안 되는 이유도 설명해줘
```

**3단계 — 조립**

```
방금 만든 집계에 RANK() 로 순위를 붙이고, employee/branch 를 조인해서
최종 결과를 만들어줘
```

**4단계 — 자가 검증 시키기**

```
지금 쿼리에서 퇴직자를 거르는 조건이 순위를 매기기 전인지 후인지 확인해줘.
후라면 무슨 문제가 생기는지도 설명해줘
```

---

## C. 검증용 프롬프트 (둘 다에게)

답을 받은 뒤 **반드시** 이걸 물어보세요. 설명을 못 하면 그 쿼리는 못 믿습니다.

```
이 쿼리에서 LEFT JOIN 을 INNER JOIN 으로 바꾸면 결과가 어떻게 달라지는지 설명해줘
```

```
기간 조건을 WHERE 에 두는 것과 ON 에 두는 것의 차이를 이 쿼리 기준으로 설명해줘
```

```
이 쿼리 결과의 행 수가 몇 개일지 예상하고, 왜 그런지 설명해줘
```
'''

# ═══════════════════════════════════════════════════ 비교 보고서 MD
REPORT_MD = '''# 정답본 vs Qwen3.6-35B 비교 보고서

가상 은행 「한빛은행」 집계 쿼리 2문제 · SBTI 과정 실습

> **은행명 · 직원명 · 사번 · 영업점 · 상품명 · 고객번호 · 수치 전부 지어낸 값입니다.**
> 실제 상품·직원·시스템과 아무 관련이 없습니다.

---

## 이 보고서의 상태

| 칸 | 상태 |
|---|---|
| 정답 쿼리 | **작성 완료** (Claude 작성 · `정답/` 폴더) |
| 채점 기준 | **작성 완료** |
| Qwen3.6-35B 결과 | **비어 있음 — 직접 실행해서 채워야 합니다** |

Qwen 결과는 **실제로 돌려서** 붙여넣으세요.
아래 「예상 실패 지점」은 일반적인 소형 모델의 경향을 적은 **가설**이며,
실측값이 아닙니다. 실행 결과가 다르면 실행 결과가 맞습니다.

---

## 실습 순서

1. `schema/01-테이블생성.sql` → `schema/02-더미데이터.sql` 실행
2. `예시프롬프트.md` 의 **A. 한 번에 물어보기** 를 Claude 와 Qwen 에 **똑같이** 입력
3. 두 결과를 아래 표에 붙여넣기
4. 실제로 실행해서 결과 행 수 · 값 비교
5. Qwen 이 틀렸으면 **B. 나눠서 물어보기** 로 다시 시도 → 되는지 기록

---

# 문제 1 · 카드 추천실적 상위 10명

## 요건 요약

- 2026 상반기 · 카드 상품 · `ref_status='NORMAL'` 만 실적
- 재직자만 · 추천건수 → 추천고객수 → 사번 순 정렬
- **상위 10명, 단 10위 동점자 포함**
- 출력 9개 컬럼 (취소건수·취소율 포함)

## 채점 기준 (5점)

| # | 항목 | 배점 | 확인 방법 |
|---|---|---:|---|
| 1 | 동점 처리 — `RANK()` 사용 (`LIMIT 10` 아님) | 1 | `RANK` 가 있는가, 정렬키에 사번 같은 고유값이 섞이지 않았는가 |
| 2 | `COUNT(DISTINCT cust_no)` 로 고객수 별도 계산 | 1 | 건수와 고객수가 다른 값으로 나오는가 |
| 3 | 취소건수를 `FILTER`/`CASE` 로 같이 집계 | 1 | `WHERE ref_status='NORMAL'` 로 걸어버리지 않았는가 |
| 4 | 재직자 필터가 **집계 전** | 1 | 순위에 구멍(1,2,4,5…)이 없는가 |
| 5 | 취소율 0 나눗셈 방어 | 1 | `NULLIF` 또는 `CASE` 가 있는가 |

## 정답 쿼리

`정답/정답1_카드추천실적_상위10명.sql` 참조.

```sql
WITH card_ref AS (
    SELECT r.ref_emp_no, r.cust_no, r.ref_status
    FROM referral r
    JOIN product  p ON p.prod_cd = r.prod_cd
    JOIN employee e ON e.emp_no  = r.ref_emp_no
    WHERE p.prod_type = 'CARD'
      AND e.emp_status = '재직'
      AND r.apply_dt >= DATE '2026-01-01'
      AND r.apply_dt <  DATE '2026-07-01'
),
agg AS (
    SELECT ref_emp_no,
           COUNT(*) FILTER (WHERE ref_status = 'NORMAL')                 AS 추천건수,
           COUNT(DISTINCT cust_no) FILTER (WHERE ref_status = 'NORMAL')  AS 추천고객수,
           COUNT(*) FILTER (WHERE ref_status = 'CANCELLED')              AS 취소건수
    FROM card_ref GROUP BY ref_emp_no
),
ranked AS (
    SELECT a.*, RANK() OVER (ORDER BY a.추천건수 DESC) AS 순위
    FROM agg a WHERE a.추천건수 > 0
)
SELECT r.순위, r.ref_emp_no AS 사번, e.emp_nm AS 직원명, b.branch_nm AS 영업점명,
       e.position AS 직급, r.추천건수, r.추천고객수, r.취소건수,
       ROUND(r.취소건수 * 100.0 / NULLIF(r.추천건수 + r.취소건수, 0), 1) AS "취소율(%)"
FROM ranked r
JOIN employee e ON e.emp_no    = r.ref_emp_no
JOIN branch   b ON b.branch_cd = e.branch_cd
WHERE r.순위 <= 10
ORDER BY r.순위, r.추천고객수 DESC, r.ref_emp_no;
```

## 검증된 정답 결과 (실행 확인)

**12행** 이 나옵니다. 10행이 아닙니다 — 공동 10위가 3명이라 12행입니다.

| 순위 | 사번 | 직원명 | 영업점 | 건수 | 고객수 | 취소 | 취소율 |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | 1000001 | 김하늘 | 한빛 본점 | 52 | 47 | 6 | 10.3 |
| 1 | 1000023 | 양하람 | 한빛 부산서면지점 | 52 | 47 | 2 | 3.7 |
| 3 | 1000007 | 윤노을 | 한빛 여의도지점 | 47 | 42 | 5 | 9.6 |
| 4 | 1000016 | 권도담 | 한빛 대전둔산지점 | 45 | 40 | 3 | 6.3 |
| 5 | 1000004 | 최나무 | 한빛 본점 | 43 | 38 | 7 | 14.0 |
| 6 | 1000011 | 신여울 | 한빛 판교지점 | 41 | 36 | 2 | 4.7 |
| 7 | 1000020 | 명가람 | 한빛 광주상무지점 | 39 | 34 | 4 | 9.3 |
| 8 | 1000026 | 장미소 | 한빛 창원지점 | 37 | 32 | 1 | 2.6 |
| 9 | 1000009 | 한소망 | 한빛 판교지점 | 35 | 30 | 3 | 7.9 |
| 10 | 1000013 | 임소울 | 한빛 강릉지점 | 33 | 28 | 2 | 5.7 |
| 10 | 1000021 | 반슬기 | 한빛 광주상무지점 | 33 | 28 | 5 | 13.2 |
| 10 | 1000034 | 황단비 | 한빛 광주상무지점 | 33 | 28 | 0 | 0.0 |

**틀리면 이렇게 나옵니다 (실행으로 확인)**

| 실수 | 증상 |
|---|---|
| `LIMIT 10` 사용 | 10행. 공동 10위 3명 중 1명이 조용히 잘림 |
| 재직 필터 누락 | 3위에 **퇴직자 남해린(1000018, 50건)** 이 끼어듦 |
| 날짜 필터 누락 | 전원 60건으로 뭉개져 순위가 1개 값이 됨 |
| `WHERE ref_status='NORMAL'` | 취소건수가 전부 0 |
| 고객수를 `COUNT(*)` 로 | 고객수가 건수와 동일해짐 (정답은 5 작음) |

## Qwen3.6-35B 결과 — 여기에 붙여넣으세요

```sql
-- (Qwen 이 만든 쿼리를 그대로 붙여넣기)



```

| 채점 항목 | 통과 여부 | 메모 |
|---|:---:|---|
| 1. RANK 사용 | ☐ | |
| 2. DISTINCT 고객수 | ☐ | |
| 3. 취소건수 동시 집계 | ☐ | |
| 4. 재직자 필터 위치 | ☐ | |
| 5. 0 나눗셈 방어 | ☐ | |
| **실행 결과 행 수** | | 정답: ____ / Qwen: ____ |

## 예상 실패 지점 (가설 — 실측 아님)

- `LIMIT 10` 으로 처리해 동점자가 잘릴 가능성
- 취소건수를 세려고 `referral` 을 **한 번 더 조인/서브쿼리**로 읽을 가능성
- 재직자 조건을 마지막 `WHERE` 에 붙여 순위에 구멍이 생길 가능성

---

# 문제 2 · 앱 페이지뷰 집계

## 요건 요약

- 2026년 7월 · 폐쇄 페이지 제외
- PV / UV(비로그인 제외) / 세션수 / 평균체류초
- **조회 0건 페이지도 0으로 표시**
- PV 내림차순 상위 20

## 채점 기준 (5점)

| # | 항목 | 배점 | 확인 방법 |
|---|---|---:|---|
| 1 | `LEFT JOIN` 사용 | 1 | `INNER` 가 아닌가 |
| 2 | **기간 조건이 `ON` 절에** | 1 | `WHERE` 에 있으면 0건 페이지가 사라진다 |
| 3 | `COUNT(l.log_id)` (`COUNT(*)` 아님) | 1 | 0건 페이지의 PV 가 0 인가, 1 인가 |
| 4 | UV = `COUNT(DISTINCT cust_no)` | 1 | 비로그인이 빠졌는가 |
| 5 | 평균체류 `COALESCE` | 1 | 0건 페이지가 NULL 인가 0 인가 |

## 정답 쿼리

`정답/정답2_앱페이지뷰_집계.sql` 참조.

```sql
SELECT p.page_cd AS 페이지코드, p.page_nm AS 페이지명, p.category AS 카테고리,
       COUNT(l.log_id)              AS "PV",
       COUNT(DISTINCT l.cust_no)    AS "UV",
       COUNT(DISTINCT l.session_id) AS 세션수,
       COALESCE(ROUND(AVG(l.stay_sec)::numeric, 1), 0) AS 평균체류초
FROM app_page p
LEFT JOIN page_view_log l
       ON l.page_id  = p.page_id
      AND l.view_at >= TIMESTAMP '2026-07-01 00:00:00'
      AND l.view_at <  TIMESTAMP '2026-08-01 00:00:00'
WHERE p.close_dt IS NULL OR p.close_dt >= DATE '2026-07-01'
GROUP BY p.page_cd, p.page_nm, p.category, p.page_id
ORDER BY "PV" DESC, p.page_id
LIMIT 20;
```

## 검증된 정답 결과 (실행 확인)

`LIMIT 20` 을 빼면 **988행**(운영중 페이지 수), 그중 **376행이 PV=0** 입니다.

| 페이지코드 | 페이지명 | 카테고리 | PV | UV | 세션수 | 평균체류초 |
|---|---|---|---:|---:|---:|---:|
| PG0001 | 홈 | 홈 | 33,793 | 3,999 | 28,084 | 152.9 |
| PG0002 | 전체계좌조회 | 자산 | 10,204 | 3,499 | 9,628 | 151.4 |
| PG0003 | 이체하기 | 이체 | 7,440 | 3,116 | 7,129 | 151.8 |
| PG0004 | 자주쓰는 이체 | 이체 | 6,094 | 2,852 | 5,894 | 153.5 |
| PG0005 | 프리미어 라운지 | 혜택 | 5,170 | 2,608 | 5,040 | 152.0 |

**틀리면 이렇게 나옵니다 (실행으로 확인)**

| 실수 | 증상 |
|---|---|
| 기간조건을 `WHERE` 에 | 988행 → **612행**. 376개 페이지가 사라짐 |
| `COUNT(*)` 사용 | PV=0 페이지 376개가 전부 **PV=1** 로 나옴 |
| `INNER JOIN` | 기간조건을 WHERE 에 둔 것과 동일 |
| 폐쇄 페이지 조건 누락 | 1,000행 (988 + 폐쇄 12) |

> **가장 무서운 건 첫 번째입니다.** 에러도 안 나고 상위 20개는 정답과 완전히 같아서
> `LIMIT 20` 결과만 보면 **절대 못 잡습니다.**
> `LIMIT` 을 빼고 `COUNT(*)` 로 감싸 988 이 나오는지 확인해야 합니다.

## Qwen3.6-35B 결과 — 여기에 붙여넣으세요

```sql
-- (Qwen 이 만든 쿼리를 그대로 붙여넣기)



```

| 채점 항목 | 통과 여부 | 메모 |
|---|:---:|---|
| 1. LEFT JOIN | ☐ | |
| 2. 기간 조건 ON 절 | ☐ | |
| 3. COUNT(컬럼) | ☐ | |
| 4. UV DISTINCT | ☐ | |
| 5. COALESCE | ☐ | |
| **PV=0 페이지 포함 여부** | | 정답: 포함 / Qwen: ____ |

## 예상 실패 지점 (가설 — 실측 아님)

- 기간 조건을 `WHERE` 에 두어 `LEFT JOIN` 이 `INNER` 처럼 동작할 가능성 — **가장 흔한 실수**
- `COUNT(*)` 를 써서 조회 0건 페이지의 PV 가 1 로 나올 가능성
- UV 와 세션수를 구분하지 않고 하나로 합칠 가능성

---

# 종합 기록

| | 문제 1 | 문제 2 |
|---|:---:|:---:|
| Claude (한 번에) | / 5 | / 5 |
| Qwen 3.6 35B (한 번에) | / 5 | / 5 |
| Qwen 3.6 35B (나눠서 · 프롬프트 B) | / 5 | / 5 |

## 마무리 질문

1. 한 번에 시켰을 때 두 모델의 차이가 가장 크게 난 항목은 무엇이었나?
2. Qwen 이 **나눠서 물어보니 맞힌** 항목이 있었나? 있었다면 어떤 프롬프트가 통했나?
3. 두 모델 다 놓친 항목이 있었나? (있다면 그게 사람이 반드시 봐야 하는 지점이다)
4. 이 결과를 보고, 실무에서 AI가 만든 집계 쿼리를 어디까지 믿을 것인가?
'''

F['비교보고서.md'] = REPORT_MD

# ═══════════════════════════════════════════════════ HTML 보고서
F['비교보고서.html'] = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>정답본 vs Qwen3.6-35B 비교 보고서</title>
<style>
:root{--blue:#0066cc;--line:#e2e7ee;--muted:#5f6672;--bad:#dc2626;--good:#16a34a;--amber:#b45309;
--mono:ui-monospace,SFMono-Regular,Menlo,monospace;
--font:-apple-system,BlinkMacSystemFont,"Pretendard","Segoe UI",sans-serif}
*{box-sizing:border-box}
body{margin:0;padding:38px 24px 70px;background:#f7f9fc;color:#1a1a1a;font-family:var(--font);line-height:1.62}
.wrap{max-width:1120px;margin:0 auto}
h1{font-size:29px;letter-spacing:-.03em;margin:0 0 5px}
.sub{color:var(--muted);margin:0 0 12px;font-size:15px}
.warn{background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;border-radius:12px;padding:11px 16px;
font-size:13.5px;font-weight:700;margin:0 0 12px}
.status{background:#fff;border:1px solid var(--line);border-radius:12px;padding:4px 18px;margin:0 0 30px}
h2{font-size:22px;margin:40px 0 10px;letter-spacing:-.02em;padding-top:14px;border-top:2px solid #e8eef7}
h3{font-size:16px;margin:26px 0 8px;color:#0f172a}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13.5px;background:#fff}
th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
th{background:#f4f7fb;font-weight:800}
td code,th code{font:600 12px var(--mono);background:#f4f7fb;border-radius:4px;padding:1px 5px}
pre{background:#0f172a;color:#e2e8f0;border-radius:12px;padding:16px 18px;overflow-x:auto;
font:600 12.3px/1.6 var(--mono);margin:10px 0}
pre.blank{background:#fff;color:#94a3b8;border:2px dashed #cbd5e1;min-height:120px}
.k{color:#7dd3fc}.s{color:#fca5a5}.c{color:#94a3b8;font-style:italic}.f{color:#fcd34d}
.tag{display:inline-block;font:900 11px var(--mono);border-radius:999px;padding:3px 10px;margin-right:7px;vertical-align:2px}
.tag.done{background:#dcfce7;color:#15803d}
.tag.todo{background:#fee2e2;color:#b91c1c}
.tag.guess{background:#fef3c7;color:var(--amber)}
.note{background:#fff;border-left:4px solid var(--blue);border-radius:0 10px 10px 0;
padding:12px 16px;margin:12px 0;font-size:13.5px}
.note.amber{border-left-color:var(--amber);background:#fffbeb}
.steps{display:grid;grid-template-columns:repeat(5,1fr);gap:9px;margin:14px 0}
.step{background:#fff;border:1px solid var(--line);border-radius:12px;padding:13px 14px;font-size:13px}
.step b{display:inline-grid;place-items:center;width:23px;height:23px;border-radius:7px;
background:var(--blue);color:#fff;font:900 12px var(--mono);margin-bottom:7px}
.foot{margin-top:46px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:12.5px}
@media(max-width:820px){.steps{grid-template-columns:1fr 1fr}}
</style></head><body><div class="wrap">

<h1>정답본 vs Qwen3.6-35B 비교 보고서</h1>
<p class="sub">가상 은행 「한빛은행」 집계 쿼리 2문제 · SBTI 과정 실습</p>
<p class="warn">※ 은행명 · 직원명 · 사번 · 영업점 · 상품명 · 고객번호 · 수치 전부 지어낸 값입니다. 실제 상품·직원·시스템과 무관합니다.</p>

<div class="status">
<table style="margin:10px 0">
<tr><th style="width:180px">칸</th><th>상태</th></tr>
<tr><td>정답 쿼리</td><td><span class="tag done">작성 완료</span> Claude 작성 · <code>정답/</code> 폴더</td></tr>
<tr><td>채점 기준</td><td><span class="tag done">작성 완료</span> 문제당 5점</td></tr>
<tr><td>Qwen3.6-35B 결과</td><td><span class="tag todo">비어 있음</span> 직접 실행해서 채워야 합니다</td></tr>
</table>
</div>

<div class="note amber">
<b>Qwen 결과는 실제로 돌려서 붙여넣으세요.</b><br>
이 문서의 「예상 실패 지점」은 일반적인 소형 모델의 경향을 적은 <b>가설</b>이며 실측값이 아닙니다.
실행 결과가 다르면 실행 결과가 맞습니다.
</div>

<h2>실습 순서</h2>
<div class="steps">
<div class="step"><b>1</b>스키마 · 더미데이터 실행</div>
<div class="step"><b>2</b>같은 프롬프트를 Claude / Qwen 에 입력</div>
<div class="step"><b>3</b>두 결과를 아래에 붙여넣기</div>
<div class="step"><b>4</b>실제 실행해서 행 수 · 값 비교</div>
<div class="step"><b>5</b>틀렸으면 나눠서 재시도 → 기록</div>
</div>

<h2>문제 1 · 카드 추천실적 상위 10명 <span style="font-size:15px;font-weight:400;color:var(--muted)">★★★</span></h2>

<p style="font-size:14px">2026 상반기 · 카드 상품 · <code>ref_status='NORMAL'</code> 만 실적 · 재직자만 ·
<b>상위 10명이되 10위 동점자 포함</b> · 출력 9개 컬럼</p>

<h3>채점 기준 (5점)</h3>
<table>
<tr><th style="width:34px">#</th><th>항목</th><th style="width:46%">확인 방법</th></tr>
<tr><td>1</td><td>동점 처리 — <code>RANK()</code> 사용 (<code>LIMIT 10</code> 아님)</td><td><code>RANK</code> 가 있는가, <b>정렬키에 사번 같은 고유값이 섞이면 동점이 사라진다</b></td></tr>
<tr><td>2</td><td><code>COUNT(DISTINCT cust_no)</code> 로 고객수 별도 계산</td><td>건수와 고객수가 다른 값인가</td></tr>
<tr><td>3</td><td>취소건수를 <code>FILTER</code>/<code>CASE</code> 로 같이 집계</td><td><code>WHERE ref_status='NORMAL'</code> 로 걸어버리지 않았는가</td></tr>
<tr><td>4</td><td>재직자 필터가 <b>집계 전</b></td><td>순위에 구멍(1,2,4,5…)이 없는가</td></tr>
<tr><td>5</td><td>취소율 0 나눗셈 방어</td><td><code>NULLIF</code> 또는 <code>CASE</code> 가 있는가</td></tr>
</table>

<h3>정답 쿼리 <span class="tag done">Claude</span></h3>
<pre><span class="k">WITH</span> card_ref <span class="k">AS</span> (
    <span class="k">SELECT</span> r.ref_emp_no, r.cust_no, r.ref_status
    <span class="k">FROM</span> referral r
    <span class="k">JOIN</span> product  p <span class="k">ON</span> p.prod_cd = r.prod_cd
    <span class="k">JOIN</span> employee e <span class="k">ON</span> e.emp_no  = r.ref_emp_no
    <span class="k">WHERE</span> p.prod_type = <span class="s">'CARD'</span>
      <span class="k">AND</span> e.emp_status = <span class="s">'재직'</span>              <span class="c">-- 순위 매기기 "전"에 제외</span>
      <span class="k">AND</span> r.apply_dt &gt;= <span class="k">DATE</span> <span class="s">'2026-01-01'</span>
      <span class="k">AND</span> r.apply_dt &lt;  <span class="k">DATE</span> <span class="s">'2026-07-01'</span>    <span class="c">-- &lt; 7월 1일</span>
),
agg <span class="k">AS</span> (
    <span class="k">SELECT</span> ref_emp_no,
           <span class="k">COUNT</span>(*) <span class="f">FILTER (WHERE</span> ref_status = <span class="s">'NORMAL'</span><span class="f">)</span>                <span class="k">AS</span> 추천건수,
           <span class="k">COUNT</span>(<span class="k">DISTINCT</span> cust_no) <span class="f">FILTER (WHERE</span> ref_status = <span class="s">'NORMAL'</span><span class="f">)</span> <span class="k">AS</span> 추천고객수,
           <span class="k">COUNT</span>(*) <span class="f">FILTER (WHERE</span> ref_status = <span class="s">'CANCELLED'</span><span class="f">)</span>             <span class="k">AS</span> 취소건수
    <span class="k">FROM</span> card_ref <span class="k">GROUP BY</span> ref_emp_no
),
ranked <span class="k">AS</span> (
    <span class="k">SELECT</span> a.*, <span class="f">RANK() OVER (ORDER BY</span> a.추천건수 <span class="k">DESC</span>, a.추천고객수 <span class="k">DESC</span>, a.ref_emp_no<span class="f">)</span> <span class="k">AS</span> 순위
    <span class="k">FROM</span> agg a <span class="k">WHERE</span> a.추천건수 &gt; 0
)
<span class="k">SELECT</span> r.순위, r.ref_emp_no <span class="k">AS</span> 사번, e.emp_nm <span class="k">AS</span> 직원명, b.branch_nm <span class="k">AS</span> 영업점명,
       e.position <span class="k">AS</span> 직급, r.추천건수, r.추천고객수, r.취소건수,
       <span class="k">ROUND</span>(r.취소건수 * 100.0 / <span class="f">NULLIF</span>(r.추천건수 + r.취소건수, 0), 1) <span class="k">AS</span> <span class="s">"취소율(%)"</span>
<span class="k">FROM</span> ranked r
<span class="k">JOIN</span> employee e <span class="k">ON</span> e.emp_no    = r.ref_emp_no
<span class="k">JOIN</span> branch   b <span class="k">ON</span> b.branch_cd = e.branch_cd
<span class="k">WHERE</span> r.순위 &lt;= 10
<span class="k">ORDER BY</span> r.순위;</pre>

<h3>검증된 정답 결과 <span class="tag done">실행 확인</span></h3>
<p style="font-size:14px"><b>12행</b>이 나옵니다. 10행이 아닙니다 — 공동 10위가 3명이라 12행입니다.</p>
<table>
<tr><th>순위</th><th>사번</th><th>직원명</th><th>영업점</th><th>건수</th><th>고객수</th><th>취소</th><th>취소율</th></tr>
<tr><td>1</td><td>1000001</td><td>김하늘</td><td>한빛 본점</td><td>52</td><td>47</td><td>6</td><td>10.3</td></tr>
<tr><td>1</td><td>1000023</td><td>양하람</td><td>한빛 부산서면지점</td><td>52</td><td>47</td><td>2</td><td>3.7</td></tr>
<tr><td>3</td><td>1000007</td><td>윤노을</td><td>한빛 여의도지점</td><td>47</td><td>42</td><td>5</td><td>9.6</td></tr>
<tr><td>4</td><td>1000016</td><td>권도담</td><td>한빛 대전둔산지점</td><td>45</td><td>40</td><td>3</td><td>6.3</td></tr>
<tr><td>5</td><td>1000004</td><td>최나무</td><td>한빛 본점</td><td>43</td><td>38</td><td>7</td><td>14.0</td></tr>
<tr><td>6</td><td>1000011</td><td>신여울</td><td>한빛 판교지점</td><td>41</td><td>36</td><td>2</td><td>4.7</td></tr>
<tr><td>7</td><td>1000020</td><td>명가람</td><td>한빛 광주상무지점</td><td>39</td><td>34</td><td>4</td><td>9.3</td></tr>
<tr><td>8</td><td>1000026</td><td>장미소</td><td>한빛 창원지점</td><td>37</td><td>32</td><td>1</td><td>2.6</td></tr>
<tr><td>9</td><td>1000009</td><td>한소망</td><td>한빛 판교지점</td><td>35</td><td>30</td><td>3</td><td>7.9</td></tr>
<tr><td>10</td><td>1000013</td><td>임소울</td><td>한빛 강릉지점</td><td>33</td><td>28</td><td>2</td><td>5.7</td></tr>
<tr><td>10</td><td>1000021</td><td>반슬기</td><td>한빛 광주상무지점</td><td>33</td><td>28</td><td>5</td><td>13.2</td></tr>
<tr><td>10</td><td>1000034</td><td>황단비</td><td>한빛 광주상무지점</td><td>33</td><td>28</td><td>0</td><td>0.0</td></tr>
</table>
<table>
<tr><th style="width:36%">실수</th><th>증상 (실행으로 확인)</th></tr>
<tr><td><code>LIMIT 10</code> 사용</td><td>10행. 공동 10위 3명 중 1명이 조용히 잘림</td></tr>
<tr><td>재직 필터 누락</td><td>3위에 <b>퇴직자 남해린(1000018, 50건)</b> 이 끼어듦</td></tr>
<tr><td>날짜 필터 누락</td><td>전원 60건으로 뭉개져 순위가 1개 값이 됨</td></tr>
<tr><td><code>WHERE ref_status='NORMAL'</code></td><td>취소건수가 전부 0</td></tr>
<tr><td>고객수를 <code>COUNT(*)</code> 로</td><td>고객수가 건수와 동일해짐 (정답은 5 작음)</td></tr>
</table>

<h3>Qwen3.6-35B 결과 <span class="tag todo">붙여넣기</span></h3>
<pre class="blank">-- Qwen 이 만든 쿼리를 그대로 붙여넣으세요</pre>

<table>
<tr><th style="width:52%">채점 항목</th><th style="width:90px">통과</th><th>메모</th></tr>
<tr><td>1. RANK 사용</td><td>☐</td><td></td></tr>
<tr><td>2. DISTINCT 고객수</td><td>☐</td><td></td></tr>
<tr><td>3. 취소건수 동시 집계</td><td>☐</td><td></td></tr>
<tr><td>4. 재직자 필터 위치</td><td>☐</td><td></td></tr>
<tr><td>5. 0 나눗셈 방어</td><td>☐</td><td></td></tr>
<tr><td><b>실행 결과 행 수</b></td><td colspan="2">정답 ____ / Qwen ____</td></tr>
</table>

<div class="note"><span class="tag guess">가설</span>
<b>예상 실패 지점</b> — 실측 아님. 실행 결과가 다르면 실행 결과가 맞습니다.<br>
· <code>LIMIT 10</code> 으로 처리해 동점자가 잘릴 가능성<br>
· 취소건수를 세려고 <code>referral</code> 을 한 번 더 조인/서브쿼리로 읽을 가능성<br>
· 재직자 조건을 마지막 <code>WHERE</code> 에 붙여 순위에 구멍이 생길 가능성
</div>

<h2>문제 2 · 앱 페이지뷰 집계 <span style="font-size:15px;font-weight:400;color:var(--muted)">★★★</span></h2>

<p style="font-size:14px">2026년 7월 · 폐쇄 페이지 제외 · PV / UV(비로그인 제외) / 세션수 / 평균체류초 ·
<b>조회 0건 페이지도 0으로 표시</b> · PV 내림차순 상위 20</p>

<h3>채점 기준 (5점)</h3>
<table>
<tr><th style="width:34px">#</th><th>항목</th><th style="width:46%">확인 방법</th></tr>
<tr><td>1</td><td><code>LEFT JOIN</code> 사용</td><td><code>INNER</code> 가 아닌가</td></tr>
<tr><td>2</td><td><b>기간 조건이 <code>ON</code> 절에</b></td><td><code>WHERE</code> 에 있으면 0건 페이지가 사라진다</td></tr>
<tr><td>3</td><td><code>COUNT(l.log_id)</code> (<code>COUNT(*)</code> 아님)</td><td>0건 페이지의 PV 가 0 인가 1 인가</td></tr>
<tr><td>4</td><td>UV = <code>COUNT(DISTINCT cust_no)</code></td><td>비로그인이 빠졌는가</td></tr>
<tr><td>5</td><td>평균체류 <code>COALESCE</code></td><td>0건 페이지가 NULL 인가 0 인가</td></tr>
</table>

<h3>정답 쿼리 <span class="tag done">Claude</span></h3>
<pre><span class="k">SELECT</span> p.page_cd <span class="k">AS</span> 페이지코드, p.page_nm <span class="k">AS</span> 페이지명, p.category <span class="k">AS</span> 카테고리,
       <span class="k">COUNT</span>(<span class="f">l.log_id</span>)              <span class="k">AS</span> <span class="s">"PV"</span>      <span class="c">-- COUNT(*) 아님</span>
       , <span class="k">COUNT</span>(<span class="k">DISTINCT</span> l.cust_no)    <span class="k">AS</span> <span class="s">"UV"</span>
       , <span class="k">COUNT</span>(<span class="k">DISTINCT</span> l.session_id) <span class="k">AS</span> 세션수
       , <span class="f">COALESCE</span>(<span class="k">ROUND</span>(<span class="k">AVG</span>(l.stay_sec)::numeric, 1), 0) <span class="k">AS</span> 평균체류초
<span class="k">FROM</span> app_page p
<span class="f">LEFT JOIN</span> page_view_log l
       <span class="f">ON</span> l.page_id  = p.page_id
      <span class="f">AND</span> l.view_at &gt;= <span class="k">TIMESTAMP</span> <span class="s">'2026-07-01 00:00:00'</span>
      <span class="f">AND</span> l.view_at &lt;  <span class="k">TIMESTAMP</span> <span class="s">'2026-08-01 00:00:00'</span>   <span class="c">-- ★ 기간 조건은 ON 절에</span>
<span class="k">WHERE</span> p.close_dt <span class="k">IS NULL</span> <span class="k">OR</span> p.close_dt &gt;= <span class="k">DATE</span> <span class="s">'2026-07-01'</span>
<span class="k">GROUP BY</span> p.page_cd, p.page_nm, p.category, p.page_id
<span class="k">ORDER BY</span> <span class="s">"PV"</span> <span class="k">DESC</span>, p.page_id
<span class="k">LIMIT</span> 20;</pre>

<div class="note">
<b>이 문제의 핵심은 ② 입니다.</b>
기간 조건을 <code>WHERE</code> 에 두면 로그가 없는 페이지는 <code>view_at</code> 이 NULL 이라 조건에서 탈락합니다.
<code>LEFT JOIN</code> 이 사실상 <code>INNER JOIN</code> 이 되어 <b>조회 0건 페이지가 통째로 사라집니다.</b>
쿼리는 에러 없이 돌고 결과도 그럴듯해서 <b>눈으로는 못 잡습니다.</b>
</div>

<h3>검증된 정답 결과 <span class="tag done">실행 확인</span></h3>
<p style="font-size:14px"><code>LIMIT 20</code> 을 빼면 <b>988행</b>(운영중 페이지 수), 그중 <b>376행이 PV=0</b> 입니다.</p>
<table>
<tr><th>페이지코드</th><th>페이지명</th><th>카테고리</th><th>PV</th><th>UV</th><th>세션수</th><th>평균체류초</th></tr>
<tr><td>PG0001</td><td>홈</td><td>홈</td><td>33,793</td><td>3,999</td><td>28,084</td><td>152.9</td></tr>
<tr><td>PG0002</td><td>전체계좌조회</td><td>자산</td><td>10,204</td><td>3,499</td><td>9,628</td><td>151.4</td></tr>
<tr><td>PG0003</td><td>이체하기</td><td>이체</td><td>7,440</td><td>3,116</td><td>7,129</td><td>151.8</td></tr>
<tr><td>PG0004</td><td>자주쓰는 이체</td><td>이체</td><td>6,094</td><td>2,852</td><td>5,894</td><td>153.5</td></tr>
<tr><td>PG0005</td><td>프리미어 라운지</td><td>혜택</td><td>5,170</td><td>2,608</td><td>5,040</td><td>152.0</td></tr>
</table>
<table>
<tr><th style="width:36%">실수</th><th>증상 (실행으로 확인)</th></tr>
<tr><td>기간조건을 <code>WHERE</code> 에</td><td>988행 → <b>612행</b>. 376개 페이지가 사라짐</td></tr>
<tr><td><code>COUNT(*)</code> 사용</td><td>PV=0 페이지 376개가 전부 <b>PV=1</b> 로 나옴</td></tr>
<tr><td><code>INNER JOIN</code></td><td>기간조건을 WHERE 에 둔 것과 동일</td></tr>
<tr><td>폐쇄 페이지 조건 누락</td><td>1,000행 (988 + 폐쇄 12)</td></tr>
</table>
<div class="note amber"><b>가장 무서운 건 첫 번째입니다.</b>
에러도 안 나고 <b>상위 20개는 정답과 완전히 같아서</b> <code>LIMIT 20</code> 결과만 보면 절대 못 잡습니다.
<code>LIMIT</code> 을 빼고 <code>COUNT(*)</code> 로 감싸 988 이 나오는지 확인해야 합니다.</div>

<h3>Qwen3.6-35B 결과 <span class="tag todo">붙여넣기</span></h3>
<pre class="blank">-- Qwen 이 만든 쿼리를 그대로 붙여넣으세요</pre>

<table>
<tr><th style="width:52%">채점 항목</th><th style="width:90px">통과</th><th>메모</th></tr>
<tr><td>1. LEFT JOIN</td><td>☐</td><td></td></tr>
<tr><td>2. 기간 조건 ON 절</td><td>☐</td><td></td></tr>
<tr><td>3. COUNT(컬럼)</td><td>☐</td><td></td></tr>
<tr><td>4. UV DISTINCT</td><td>☐</td><td></td></tr>
<tr><td>5. COALESCE</td><td>☐</td><td></td></tr>
<tr><td><b>PV=0 페이지 포함 여부</b></td><td colspan="2">정답 포함 / Qwen ____</td></tr>
</table>

<div class="note"><span class="tag guess">가설</span>
<b>예상 실패 지점</b> — 실측 아님<br>
· 기간 조건을 <code>WHERE</code> 에 두어 <code>LEFT JOIN</code> 이 <code>INNER</code> 처럼 동작할 가능성 — <b>가장 흔한 실수</b><br>
· <code>COUNT(*)</code> 를 써서 조회 0건 페이지의 PV 가 1 로 나올 가능성<br>
· UV 와 세션수를 구분하지 않고 하나로 합칠 가능성
</div>

<h2>종합 기록</h2>
<table>
<tr><th></th><th style="width:120px">문제 1</th><th style="width:120px">문제 2</th></tr>
<tr><td>Claude (한 번에)</td><td>　/ 5</td><td>　/ 5</td></tr>
<tr><td>Qwen 3.6 35B (한 번에)</td><td>　/ 5</td><td>　/ 5</td></tr>
<tr><td>Qwen 3.6 35B (나눠서 · 프롬프트 B)</td><td>　/ 5</td><td>　/ 5</td></tr>
</table>

<h3>마무리 질문</h3>
<ol style="font-size:14px">
<li>한 번에 시켰을 때 두 모델의 차이가 가장 크게 난 항목은?</li>
<li>Qwen 이 <b>나눠서 물어보니 맞힌</b> 항목이 있었나? 어떤 프롬프트가 통했나?</li>
<li>두 모델 다 놓친 항목이 있었나? <b>있다면 그게 사람이 반드시 봐야 하는 지점이다.</b></li>
<li>이 결과를 보고, 실무에서 AI가 만든 집계 쿼리를 어디까지 믿을 것인가?</li>
</ol>

<p class="foot">SBTI 과정 · 은행권 집계 실습 · 전부 가상 데이터 · 정답본은 Claude 작성, Qwen 결과는 미실행</p>

</div></body></html>
'''

F['README.md'] = '''# 은행권 집계 실습 — 정답본 vs Qwen3.6-35B

가상 은행 「한빛은행」의 실제 업무에 가까운 집계 쿼리 2문제입니다.
**같은 프롬프트를 Claude 와 온프레미스 Qwen3.6-35B 에 넣고 결과를 비교**하는 것이 목적입니다.

> 은행명 · 직원명 · 사번 · 영업점 · 상품명 · 고객번호 · 수치 전부 지어낸 값입니다.
> 실제 상품·직원·시스템과 아무 관련이 없습니다.

## 쿼리 실행 도구 — 설치 없이 바로

**`SQL실행기.html` 을 더블클릭하세요.** 그게 전부입니다.

- SQL 엔진(SQLite)이 파일 안에 들어 있습니다. **인터넷·설치·CDN 전부 불필요**
- USB 에 폴더째 담아 가도 그 폴더 안에서 그대로 돕니다
- 테이블 6개와 데이터가 열 때 자동으로 만들어집니다 (약 0.5초)
- 왼쪽 「예제 쿼리」를 누르면 정답 쿼리가 채워집니다. `Ctrl+Enter` 로 실행

> 브라우저(SQLite) 결과와 PostgreSQL 정본 결과가 **완전히 동일**합니다.
> 문제 1은 12행, 문제 2는 988행 / PV=0 376행 — 어느 쪽에서 돌려도 같은 답입니다.

PostgreSQL 로 하고 싶으면 `schema/01` → `schema/02` 를 실행하면 됩니다.
정본 SQL 은 PostgreSQL 문법(`DATE '...'`, `::numeric`),
`SQL실행기.html` 안의 예제는 SQLite 문법(`'...'`, `ROUND(x,1)`)입니다.

## 파일

```
08_은행권_집계실습/
├── SQL실행기.html              ← 더블클릭. 설치 없이 쿼리 실행
├── README.md                  ← 지금 문서
├── 예시프롬프트.md             그대로 복사해서 쓰는 프롬프트 (A/B/C)
├── 비교보고서.html             정답 vs Qwen 비교 (화면용 · 더블클릭)
├── 비교보고서.md               같은 내용 (문서용)
├── schema/
│   ├── 01-테이블생성.sql        테이블 6개 + 인덱스
│   └── 02-더미데이터.sql        직원 40 · 상품 14 · 추천실적 ~6,000
│                               앱 페이지 1,000 · 페이지뷰 로그 120,000
├── 문제/
│   ├── 문제1_카드추천실적_상위10명.sql    ★★★
│   └── 문제2_앱페이지뷰_집계.sql          ★★★
└── 정답/
    ├── 정답1_카드추천실적_상위10명.sql
    └── 정답2_앱페이지뷰_집계.sql
```

## 데이터 구성

| 테이블 | 건수 | 설명 |
|---|---:|---|
| `branch` | 8 | 영업점 |
| `employee` | 40 | 직원 (재직 36 · 휴직 2 · 퇴직 2) |
| `product` | 14 | 카드 8 + 수신 6 |
| `referral` | 약 6,000 | 가입권유(추천) 실적 — 직원별 편차 있음, 취소·반려 섞임 |
| `app_page` | 1,000 | 앱 화면 (주요 20개는 실제 이름, 나머지 자동 생성, 약 10개 폐쇄) |
| `page_view_log` | 120,000 | 2026년 7월 한 달 · 약 18% 비로그인 |

## 문제

**문제 1 — 카드 추천실적 상위 10명** ★★★
2026 상반기 카드 가입권유 실적으로 직원 랭킹을 뽑습니다.
핵심 함정은 **"상위 10명"의 동점 처리**입니다. `LIMIT 10` 은 오답입니다.

**문제 2 — 앱 페이지뷰 집계** ★★★
7월 페이지별 PV/UV/세션수를 뽑습니다.
핵심 함정은 **`LEFT JOIN` 의 기간 조건 위치**입니다.
`WHERE` 에 두면 조회 0건 페이지가 조용히 사라지는데, **에러도 안 나고 결과도 그럴듯합니다.**

## 진행 방법

1. `schema/01` → `schema/02` 실행 (PostgreSQL 기준)
2. `예시프롬프트.md` 의 **A** 를 Claude 와 Qwen 에 **똑같이** 입력
3. `비교보고서.html` 을 열고 두 결과를 붙여넣기
4. 실제로 실행해서 **행 수와 값**을 비교 — 쿼리 모양만 보면 안 됩니다
5. Qwen 이 틀렸으면 **프롬프트 B(나눠서 묻기)** 로 다시 시도하고 결과를 기록

## 미리 알아둘 것

**정답 쿼리는 채워져 있고, Qwen 결과 칸은 비어 있습니다.**
Qwen 결과는 실제로 돌려서 붙여넣으세요.
보고서의 「예상 실패 지점」은 소형 모델의 일반적 경향을 적은 **가설**이며 실측값이 아닙니다.
실행 결과가 다르면 실행 결과가 맞습니다.

**쿼리가 에러 없이 돈다고 맞는 게 아닙니다.**
이 두 문제의 오답은 전부 **에러 없이 그럴듯한 결과를 냅니다.**
그래서 채점 기준을 5개씩 정해뒀습니다. 하나씩 대조하세요.
'''


def main():
    for rel, body in F.items():
        p = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        io.open(p, 'w', encoding='utf-8').write(body)
    for dp, _, fns in os.walk(ROOT):
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            try:
                n = sum(1 for _ in io.open(p, encoding='utf-8'))
            except UnicodeDecodeError:
                continue
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
