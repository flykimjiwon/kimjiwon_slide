// ─── 데이터 정의 (PostgreSQL 정본과 동일 산식 · 전부 가상) ────────────────
const pad=(n,w)=>String(n).padStart(w,'0');
const D0=Date.UTC(2026,0,1), T0=Date.UTC(2026,6,1);
const dstr=(b,d)=>new Date(b+d*86400000).toISOString().slice(0,10);
const tstr=(m)=>new Date(T0+m*60000).toISOString().slice(0,19).replace('T',' ');
const H=(g,mul,add)=>(g*mul+add)%2147483647;

const BRANCH=[["B0101","시난 본점","수도권","1998-03-02"],["B0102","시난 여의도지점","수도권","2004-06-14"],
["B0103","시난 판교지점","수도권","2013-09-01"],["B0104","시난 강릉지점","강원","2009-04-20"],
["B0105","시난 대전둔산지점","충청","2007-11-05"],["B0106","시난 광주상무지점","호남","2011-02-28"],
["B0107","시난 부산서면지점","영남","2001-07-16"],["B0108","시난 창원지점","영남","2016-05-09"]];

const EMP=[["1000001","김하늘","B0101","과장","2013-01-07","재직"],["1000002","이바다","B0101","대리","2017-03-13","재직"],
["1000003","박구름","B0101","행원","2022-09-05","재직"],["1000004","최나무","B0101","차장","2008-11-24","재직"],
["1000005","정바람","B0102","행원","2021-06-14","재직"],["1000006","강별","B0102","대리","2016-08-01","재직"],
["1000007","윤노을","B0102","과장","2012-04-16","재직"],["1000008","서한결","B0102","행원","2023-02-20","재직"],
["1000009","한소망","B0103","대리","2018-05-28","재직"],["1000010","오늘봄","B0103","행원","2024-01-08","재직"],
["1000011","신여울","B0103","과장","2011-10-17","재직"],["1000012","문가온","B0103","행원","2022-03-21","휴직"],
["1000013","임소울","B0104","대리","2015-07-06","재직"],["1000014","조미르","B0104","행원","2023-08-14","재직"],
["1000015","배아람","B0104","지점장","2003-02-10","재직"],["1000016","권도담","B0105","과장","2010-12-06","재직"],
["1000017","류지음","B0105","행원","2021-11-29","재직"],["1000018","남해린","B0105","대리","2017-09-11","퇴직"],
["1000019","도이든","B0106","행원","2022-05-02","재직"],["1000020","명가람","B0106","과장","2014-03-24","재직"],
["1000021","반슬기","B0106","대리","2019-01-14","재직"],["1000022","설다온","B0107","행원","2023-04-03","재직"],
["1000023","양하람","B0107","차장","2006-08-21","재직"],["1000024","엄나래","B0107","대리","2018-10-15","재직"],
["1000025","우겨레","B0107","행원","2024-02-26","재직"],["1000026","장미소","B0108","과장","2012-07-09","재직"],
["1000027","전누리","B0108","행원","2021-04-19","재직"],["1000028","차보람","B0108","대리","2016-11-07","퇴직"],
["1000029","추한별","B0101","행원","2023-06-12","재직"],["1000030","표새롬","B0102","행원","2024-03-04","재직"],
["1000031","하늘찬","B0103","대리","2019-08-26","재직"],["1000032","허가람","B0104","행원","2022-12-05","재직"],
["1000033","홍이레","B0105","행원","2023-09-18","재직"],["1000034","황단비","B0106","대리","2018-02-12","재직"],
["1000035","고운결","B0107","행원","2024-05-20","재직"],["1000036","구름솔","B0108","행원","2023-01-16","재직"],
["1000037","노을빛","B0101","대리","2017-05-22","재직"],["1000038","다솔찬","B0102","과장","2013-09-30","재직"],
["1000039","라온제","B0103","행원","2022-08-08","휴직"],["1000040","마루한","B0104","대리","2019-12-02","재직"]];

const PROD=[["C001","나라지킴이 체크카드","CARD","CHECK",3.2,"2019-03-04","Y"],
["C002","새내기 첫걸음 체크카드","CARD","CHECK",null,"2021-02-15","Y"],
["C003","시난 실속 신용카드","CARD","CREDIT",null,"2018-06-01","Y"],
["C004","드림포인트 신용카드","CARD","CREDIT",null,"2020-09-10","Y"],
["C005","실버케어 체크카드","CARD","CHECK",null,"2022-04-25","Y"],
["C006","그린모빌리티 신용카드","CARD","CREDIT",null,"2023-05-30","Y"],
["C007","시난 트래블 체크카드","CARD","CHECK",null,"2024-01-11","Y"],
["C008","옛길 클래식 신용카드","CARD","CREDIT",null,"2012-08-20","N"],
["D001","행복드림 자유적금","SAVING",null,3.2,"2017-05-02","Y"],
["D002","든든플러스 정기예금","DEPOSIT",null,3.55,"2015-01-19","Y"],
["D003","새싹 청년우대적금","SAVING",null,4.1,"2021-07-07","Y"],
["D004","미래설계 연금저축","SAVING",null,null,"2019-11-13","Y"],
["D005","슬기로운 주택청약","SAVING",null,2.8,"2010-03-08","Y"],
["D006","참좋은 파킹통장","DEPOSIT",null,2.1,"2023-02-01","N"]];

const PLAN=[["1000001",52,6,30],["1000023",52,2,22],["1000018",50,4,18],["1000007",47,5,25],
["1000016",45,3,19],["1000004",43,7,28],["1000011",41,2,16],["1000020",39,4,21],
["1000026",37,1,14],["1000009",35,3,17],["1000013",33,2,12],["1000021",33,5,20],
["1000034",33,0,11],["1000006",31,3,15],["1000024",29,2,13],["1000031",27,1,18],
["1000002",26,4,24],["1000037",24,2,9],["1000038",23,3,16],["1000015",21,1,8],
["1000040",20,2,12],["1000005",18,3,10],["1000017",17,1,7],["1000019",16,2,11],
["1000027",15,1,9],["1000003",14,2,6],["1000008",13,1,8],["1000010",12,0,5],
["1000014",11,1,7],["1000022",10,2,4],["1000025",9,0,6],["1000029",8,1,3],
["1000030",7,0,5],["1000032",6,1,4],["1000033",5,0,3],["1000035",4,1,2],
["1000036",3,0,2],["1000028",19,2,10],["1000012",28,3,14],["1000039",9,1,5]];

const PAGE20=[[1,"홈","홈",1,"2019-01-01",null],[2,"전체계좌조회","자산",2,"2019-01-01",null],
[3,"이체하기","이체",2,"2019-01-01",null],[4,"자주쓰는 이체","이체",3,"2019-06-01",null],
[5,"프리미어 라운지","혜택",2,"2021-03-01",null],[6,"상품몰 메인","상품",2,"2019-01-01",null],
[7,"카드상품 목록","상품",3,"2019-01-01",null],[8,"예적금 상품 목록","상품",3,"2019-01-01",null],
[9,"나라지킴이 체크카드 상세","상품",4,"2019-03-04",null],[10,"새내기 첫걸음 체크카드 상세","상품",4,"2021-02-15",null],
[11,"내 자산 리포트","자산",2,"2020-05-01",null],[12,"소비 분석","자산",3,"2020-05-01",null],
[13,"포인트 혜택","혜택",2,"2019-01-01",null],[14,"이벤트 목록","혜택",3,"2019-01-01",null],
[15,"고객센터 메인","고객센터",2,"2019-01-01",null],[16,"자주 묻는 질문","고객센터",3,"2019-01-01",null],
[17,"알림 설정","설정",2,"2019-01-01",null],[18,"간편비밀번호 변경","설정",3,"2019-01-01",null],
[19,"구 이벤트 페이지","혜택",3,"2019-01-01","2025-12-31"],[20,"구 상품몰","상품",2,"2019-01-01","2024-06-30"]];
const PGNM=["상품 상세","거래 내역","약관 안내","신청 결과","인증 화면","혜택 상세","설정 상세","안내 팝업","조회 결과","가입 단계"];
const PGCAT=["홈","상품","이체","자산","혜택","고객센터","설정"];
const DEV=["AOS","IOS","WEB"], CH3=["창구","모바일","제휴처"];

const SCHEMA_SQL=`
CREATE TABLE branch(branch_cd TEXT PRIMARY KEY, branch_nm TEXT, region TEXT, open_dt TEXT);
CREATE TABLE employee(emp_no TEXT PRIMARY KEY, emp_nm TEXT, branch_cd TEXT, position TEXT, hire_dt TEXT, emp_status TEXT);
CREATE TABLE product(prod_cd TEXT PRIMARY KEY, prod_nm TEXT, prod_type TEXT, card_type TEXT, base_rate REAL, launch_dt TEXT, sale_yn TEXT);
CREATE TABLE referral(ref_id INTEGER PRIMARY KEY AUTOINCREMENT, ref_emp_no TEXT, cust_no TEXT, prod_cd TEXT,
 apply_dt TEXT, channel TEXT, ref_status TEXT, first_amt INTEGER);
CREATE TABLE app_page(page_id INTEGER PRIMARY KEY, page_cd TEXT, page_nm TEXT, category TEXT, depth INTEGER, open_dt TEXT, close_dt TEXT);
CREATE TABLE page_view_log(log_id INTEGER PRIMARY KEY AUTOINCREMENT, page_id INTEGER, cust_no TEXT,
 session_id TEXT, view_at TEXT, device TEXT, stay_sec INTEGER);
CREATE INDEX idx_referral_emp_dt ON referral(ref_emp_no, apply_dt);
CREATE INDEX idx_referral_prod ON referral(prod_cd);
CREATE INDEX idx_pvlog_page_time ON page_view_log(page_id, view_at);
CREATE INDEX idx_app_page_category ON app_page(category);`;

function buildDB(SQL){
  const db=new SQL.Database();
  db.run(SCHEMA_SQL); db.run('BEGIN');
  let st=db.prepare('INSERT INTO branch VALUES (?,?,?,?)'); BRANCH.forEach(r=>st.run(r)); st.free();
  st=db.prepare('INSERT INTO employee VALUES (?,?,?,?,?,?)'); EMP.forEach(r=>st.run(r)); st.free();
  st=db.prepare('INSERT INTO product VALUES (?,?,?,?,?,?,?)'); PROD.forEach(r=>st.run(r)); st.free();
  st=db.prepare('INSERT INTO referral (ref_emp_no,cust_no,prod_cd,apply_dt,channel,ref_status,first_amt) VALUES (?,?,?,?,?,?,?)');
  const base=e=>(Number(e)%1000)*1000;
  for(const [emp,card,cancel,dep] of PLAN){
    for(let s=1;s<=card;s++) st.run([emp,'C'+pad(base(emp)+((s-1)%Math.max(card-5,1))+1,9),'C00'+(1+(s%8)),dstr(D0,(s*11)%180),CH3[s%3],'NORMAL',null]);
    for(let s=1;s<=cancel;s++) st.run([emp,'C'+pad(base(emp)+900+s,9),'C00'+(1+(s%8)),dstr(D0,(s*29)%180),'창구','CANCELLED',null]);
    for(let s=1;s<=2;s++) st.run([emp,'C'+pad(base(emp)+950+s,9),'C00'+(1+(s%8)),dstr(Date.UTC(2026,1,1),s*13),'모바일','REJECTED',null]);
    for(let s=1;s<=dep;s++) st.run([emp,'C'+pad(base(emp)+700+s,9),'D00'+(1+(s%6)),dstr(D0,(s*7)%180),(s%2===0?'창구':'모바일'),'NORMAL',100000+(s%40)*50000]);
    for(let s=1;s<=Math.max(60-card,0);s++) st.run([emp,'C'+pad(base(emp)+600+s,9),'C00'+(1+(s%8)),dstr(Date.UTC(2025,6,1),(s*3)%180),'창구','NORMAL',null]);
  } st.free();
  st=db.prepare('INSERT INTO app_page VALUES (?,?,?,?,?,?,?)');
  PAGE20.forEach(r=>st.run([r[0],'PG'+pad(r[0],4),r[1],r[2],r[3],r[4],r[5]]));
  for(let g=1;g<=980;g++){const id=20+g;
    st.run([id,'PG'+pad(id,4),PGNM[g%10]+' '+id,PGCAT[g%7],2+(g%3),dstr(Date.UTC(2019,0,1),g%2200),(g%97===0?'2025-06-30':null)]);}
  st.free();
  st=db.prepare('INSERT INTO page_view_log (page_id,cust_no,session_id,view_at,device,stay_sec) VALUES (?,?,?,?,?,?)');
  for(let g=1;g<=120000;g++){
    const src=(g%3===0)?(1+(g%27000)):g;
    const pid=1+Math.floor(Math.pow(H(src,2654435761,7)/2147483647,2.6)*620);
    const cust=(H(g,1103515245,12345)%100<18)?null:'C'+pad(1+H(g,1013904223,1)%4000,9);
    st.run([pid,cust,'S'+pad(1+H(g,22695477,1)%27000,8),tstr(H(g,214013,2531011)%44640),DEV[H(g,69069,5)%3],3+H(g,1664525,1013904223)%300]);
  } st.free();
  db.run('COMMIT');
  return db;
}

// ─── 테이블 설명 (비개발자용) ────────────────────────────────────────────
const TABLE_META={
 branch:{desc:'영업점 목록',cols:[['branch_cd','지점코드','PK'],['branch_nm','지점명',''],['region','지역',''],['open_dt','개점일','']]},
 employee:{desc:'직원 명부 — 재직/휴직/퇴직 상태가 섞여 있음',cols:[['emp_no','사번(7자리)','PK'],['emp_nm','이름',''],['branch_cd','소속 지점','FK'],['position','직급',''],['hire_dt','입사일',''],['emp_status','재직 상태','']]},
 product:{desc:'상품 목록 — 카드 8종 + 예적금 6종',cols:[['prod_cd','상품코드','PK'],['prod_nm','상품명',''],['prod_type','유형(CARD/DEPOSIT/SAVING)',''],['card_type','카드 종류(CHECK/CREDIT)',''],['base_rate','기본금리',''],['launch_dt','출시일',''],['sale_yn','판매 여부','']]},
 referral:{desc:'가입권유(추천) 실적 — 직원이 고객에게 상품을 권유해 가입시킨 기록',cols:[['ref_id','실적번호','PK'],['ref_emp_no','권유 직원 사번','FK'],['cust_no','고객번호',''],['prod_cd','상품코드','FK'],['apply_dt','신청일','IX'],['channel','채널(창구/모바일/제휴처)',''],['ref_status','상태(NORMAL/CANCELLED/REJECTED)',''],['first_amt','최초입금액(카드는 NULL)','']]},
 app_page:{desc:'앱 화면 목록 1,000개 — 일부는 폐쇄됨(close_dt)',cols:[['page_id','페이지번호','PK'],['page_cd','페이지코드',''],['page_nm','페이지명',''],['category','분류','IX'],['depth','메뉴 깊이',''],['open_dt','오픈일',''],['close_dt','폐쇄일(NULL=운영중)','']]},
 app_page_view:null,
 page_view_log:{desc:'페이지 방문 로그 12만 건 — 2026년 7월 한 달치',cols:[['log_id','로그번호','PK'],['page_id','페이지번호','FK IX'],['cust_no','고객번호(NULL=비로그인)',''],['session_id','접속 세션',''],['view_at','방문 시각','IX'],['device','기기(AOS/IOS/WEB)',''],['stay_sec','머문 시간(초)','']]}};
delete TABLE_META.app_page_view;

// ─── 정답 쿼리 (SQLite, PostgreSQL 정본과 결과 동일 검증됨) ──────────────
const ANS1=`WITH agg AS (
  SELECT r.ref_emp_no,
         SUM(CASE WHEN r.ref_status='NORMAL'    THEN 1 ELSE 0 END) AS 추천건수,
         COUNT(DISTINCT CASE WHEN r.ref_status='NORMAL' THEN r.cust_no END) AS 추천고객수,
         SUM(CASE WHEN r.ref_status='CANCELLED' THEN 1 ELSE 0 END) AS 취소건수
  FROM referral r
  JOIN product  p ON p.prod_cd = r.prod_cd
  JOIN employee e ON e.emp_no  = r.ref_emp_no
  WHERE p.prod_type = 'CARD'
    AND e.emp_status = '재직'
    AND r.apply_dt >= '2026-01-01'
    AND r.apply_dt <  '2026-07-01'
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
ORDER BY r.순위, r.추천고객수 DESC, r.ref_emp_no;`;

const ANS2=`SELECT p.page_cd AS 페이지코드, p.page_nm AS 페이지명, p.category AS 카테고리,
       COUNT(l.log_id)              AS PV,
       COUNT(DISTINCT l.cust_no)    AS UV,
       COUNT(DISTINCT l.session_id) AS 세션수,
       COALESCE(ROUND(AVG(l.stay_sec),1),0) AS 평균체류초
FROM app_page p
LEFT JOIN page_view_log l
       ON l.page_id=p.page_id
      AND l.view_at >= '2026-07-01 00:00:00'
      AND l.view_at <  '2026-08-01 00:00:00'
WHERE p.close_dt IS NULL OR p.close_dt >= '2026-07-01'
GROUP BY p.page_cd, p.page_nm, p.category, p.page_id
ORDER BY PV DESC, p.page_id
LIMIT 20;            -- Oracle 은 이 줄을  FETCH FIRST 20 ROWS ONLY  로
`;

// LLM 에게 그대로 붙여넣을 프롬프트 (비개발자용)
const PROMPT1=`아래 요건대로 SQL 쿼리를 작성해줘.
Oracle 과 MySQL 8 어디서든 그대로 도는 공통 문법만 사용해줘.
(FILTER, ROWNUM, CONNECT BY 같은 한쪽 전용 문법 금지. WITH·CASE WHEN·RANK() OVER 는 사용 가능)
행 수 제한이 필요하면 LIMIT n 을 쓰고, 쿼리만 출력해줘.

[테이블]
referral  — 가입권유 실적
  ref_emp_no VARCHAR(7)   권유 직원 사번
  cust_no    VARCHAR(10)  고객번호
  prod_cd    VARCHAR(8)   상품코드
  apply_dt   DATE         신청일 ('YYYY-MM-DD')
  ref_status VARCHAR(10)  NORMAL(정상) / CANCELLED(취소) / REJECTED(반려)
employee — 직원  (emp_no VARCHAR(7) PK, emp_nm, branch_cd, position, emp_status: 재직/휴직/퇴직)
branch   — 영업점 (branch_cd PK, branch_nm, region)
product  — 상품  (prod_cd PK, prod_nm, prod_type: CARD/DEPOSIT/SAVING, card_type)

[요건]
- 2026-01-01 ~ 2026-06-30 신청분 (apply_dt 기준)
- 카드 상품만 (product.prod_type = 'CARD')
- 실적은 ref_status='NORMAL' 인 건만 인정
- 재직중인 직원만 (employee.emp_status = '재직')
- 순위는 추천건수 기준으로만 매긴다 (같으면 공동 순위)
- 순위 10 이내를 전부 출력한다. 10위가 동점이면 10명을 넘어도 전부 나와야 한다
- 출력 컬럼(순서대로): 순위, 사번, 직원명, 영업점명, 직급, 추천건수, 추천고객수, 취소건수, 취소율(%)
  * 추천고객수 = NORMAL 건의 서로 다른 고객 수
  * 취소건수 = 같은 기간·같은 직원의 CANCELLED 건수
  * 취소율 = 취소건수/(추천건수+취소건수)*100, 소수점 1자리 반올림
- 정렬: 순위, 추천고객수 내림차순, 사번 오름차순`;

const PROMPT2=`아래 요건대로 SQL 쿼리를 작성해줘.
Oracle 과 MySQL 8 어디서든 그대로 도는 공통 문법만 사용해줘.
(FILTER, ROWNUM, CONNECT BY 같은 한쪽 전용 문법 금지. WITH·CASE WHEN·윈도우 함수는 사용 가능)
행 수 제한이 필요하면 LIMIT n 을 쓰고, 쿼리만 출력해줘.

[테이블]
app_page — 앱 화면 목록
  page_id  INT PK · page_cd VARCHAR(12) · page_nm VARCHAR(60) · category VARCHAR(20)
  close_dt DATE — NULL 이면 운영중, 값이 있으면 폐쇄된 페이지
page_view_log — 방문 로그
  log_id INT PK · page_id INT · cust_no VARCHAR(10) (NULL=비로그인)
  session_id VARCHAR(32) · view_at DATETIME ('YYYY-MM-DD HH:MM:SS') · stay_sec INT

[요건]
- 2026년 7월 한 달간의 page_view_log 기준 (view_at)
- 폐쇄 페이지 제외 (close_dt IS NULL 이거나 close_dt >= '2026-07-01')
- PV = 로그 건수
- UV = 서로 다른 고객 수 (비로그인 cust_no IS NULL 은 제외)
- 세션수 = 서로 다른 session_id 수
- 평균체류초 = stay_sec 평균, 소수점 1자리 반올림 (로그 없으면 0)
- 조회가 0건인 페이지도 결과에 나와야 한다 (PV=0 으로)
- PV 내림차순, 같으면 page_id 오름차순, 상위 20개
- 출력 컬럼(순서대로): 페이지코드, 페이지명, 카테고리, PV, UV, 세션수, 평균체류초`;
