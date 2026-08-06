// ─── 공용 ────────────────────────────────────────────────────────────────
let db=null;
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

function tableHTML(res,cap){
  cap=cap||500;
  if(!res||!res.length) return '<div class="msg ok">실행 완료 — 반환된 행이 없습니다.</div>';
  const r=res[res.length-1];
  const head='<tr>'+r.columns.map(c=>'<th>'+esc(c)+'</th>').join('')+'</tr>';
  const body=r.values.slice(0,cap).map(row=>'<tr>'+row.map(v=>
    v===null?'<td class="null">NULL</td>':
    (typeof v==='number'?'<td class="num">'+v+'</td>':'<td>'+esc(v)+'</td>')).join('')+'</tr>').join('');
  return '<table class="res"><thead>'+head+'</thead><tbody>'+body+'</tbody></table>'+
    (r.values.length>cap?'<div class="msg">…앞 '+cap+'행만 표시 (전체 '+r.values.length.toLocaleString()+'행)</div>':'');
}
// ─── Oracle/MySQL 호환 레이어 ────────────────────────────────────────────
function compatSQL(sql){
  let s=sql;
  s=s.replace(/`([^`]+)`/g,'"$1"');                                   // MySQL 백틱
  s=s.replace(/\b(DATE|TIMESTAMP)\s+'([^']+)'/gi,"'$2'");              // ANSI 날짜 리터럴
  s=s.replace(/FETCH\s+FIRST\s+(\d+)\s+ROWS?\s+ONLY/gi,'LIMIT $1');    // Oracle 12c+
  s=s.replace(/\bSYSDATE\b/gi,"'2026-08-06 00:00:00'");                // 기준일 고정
  s=s.replace(/\bSYSTIMESTAMP\b/gi,"'2026-08-06 00:00:00'");
  s=s.replace(/\bCURDATE\s*\(\s*\)/gi,"'2026-08-06'");
  s=s.replace(/\bNOW\s*\(\s*\)/gi,"'2026-08-06 00:00:00'");
  s=s.replace(/\bFROM\s+DUAL\b/gi,'');                                // Oracle DUAL
  return s;
}
function hasRownum(sql){ return /\bROWNUM\b/i.test(sql); }
const ROWNUM_MSG='ROWNUM 은 Oracle 전용이라 이 실습기에서 지원되지 않습니다.\nAI에게 "ROWNUM 대신 LIMIT 이나 FETCH FIRST n ROWS ONLY 로 다시 써줘" 라고 요청하세요.';

function registerCompat(db){
  const reg=(n,f)=>{ try{ db.create_function(n,f); }catch(e){} };
  const day=v=>String(v).slice(0,10);
  reg('NVL',(a,b)=>a==null?b:a);
  reg('NVL2',(a,b,c)=>a==null?c:b);
  reg('TO_DATE',(v,f)=>v==null?null:day(v));
  reg('TO_CHAR',function(v,f){ if(v==null)return null; v=String(v);
    if(f&&/HH/i.test(f)) return v.slice(0,19);
    if(f&&/DD/i.test(f)) return v.slice(0,10);
    if(f&&/MM/i.test(f)) return v.slice(0,7);
    return v; });
  db.create_function&&(function(){ try{ db.create_function('TO_CHAR',v=>v==null?null:String(v)); }catch(e){} })();
  reg('STR_TO_DATE',(v,f)=>v==null?null:day(v));
  reg('DATE_FORMAT',function(v,f){ if(v==null)return null; v=String(v);
    if(f==='%Y-%m-%d %H:%i:%s') return v.slice(0,19);
    if(f==='%Y-%m-%d') return v.slice(0,10);
    if(f==='%Y-%m') return v.slice(0,7); if(f==='%Y') return v.slice(0,4);
    return v; });
  reg('TRUNC',function(v,u){ if(v==null)return null;
    if(typeof v==='number'){ const p=u?Math.pow(10,u):1; return Math.trunc(v*p)/p; }
    return day(v); });
  try{ db.create_function('TRUNC',v=>v==null?null:(typeof v==='number'?Math.trunc(v):day(v))); }catch(e){}
  reg('ADD_MONTHS',function(d,n){ if(d==null)return null;
    const t=new Date(day(d)+'T00:00:00Z'); t.setUTCMonth(t.getUTCMonth()+Number(n));
    return t.toISOString().slice(0,10); });
  reg('LAST_DAY',function(d){ if(d==null)return null;
    const t=new Date(day(d)+'T00:00:00Z'); t.setUTCMonth(t.getUTCMonth()+1,0);
    return t.toISOString().slice(0,10); });
  // DECODE — 인자 수별 등록 (sql.js 는 함수 length 로 arity 를 정한다)
  const dec=(a)=>{ const v=a[0]; for(let i=1;i+1<a.length;i+=2){
      if(v==a[i]||(v==null&&a[i]==null)) return a[i+1]; }
    return (a.length%2)===0 ? a[a.length-1] : null; };
  reg('DECODE',(v,s1,r1)=>dec([v,s1,r1]));
  reg('DECODE',(v,s1,r1,d)=>dec([v,s1,r1,d]));
  reg('DECODE',(v,s1,r1,s2,r2)=>dec([v,s1,r1,s2,r2]));
  reg('DECODE',(v,s1,r1,s2,r2,d)=>dec([v,s1,r1,s2,r2,d]));
  reg('GREATEST',(a,b)=>a==null||b==null?null:(a>b?a:b));
  reg('GREATEST',(a,b,c)=>[a,b,c].some(x=>x==null)?null:[a,b,c].sort((x,y)=>x>y?-1:1)[0]);
  reg('LEAST',(a,b)=>a==null||b==null?null:(a<b?a:b));
  reg('LEAST',(a,b,c)=>[a,b,c].some(x=>x==null)?null:[a,b,c].sort((x,y)=>x<y?-1:1)[0]);
  reg('CONCAT',(a,b)=>(a==null?'':String(a))+(b==null?'':String(b)));
  reg('CONCAT',(a,b,c)=>(a==null?'':String(a))+(b==null?'':String(b))+(c==null?'':String(c)));
}
function runSQL(sql){ return db.exec(compatSQL(sql)); }

// 값 정규화: 숫자는 소수 1자리 반올림 문자열, NULL 은 ∅
function normCell(v){
  if(v===null||v===undefined) return '∅';
  if(typeof v==='number') return String(Math.round(v*10)/10);
  const t=String(v).trim();
  if(/^-?\d+(\.\d+)?$/.test(t)) return String(Math.round(parseFloat(t)*10)/10);
  return t;
}
function rowSigs(values){ return values.map(r=>r.map(normCell).join('')); }
function multisetEq(a,b){
  if(a.length!==b.length) return false;
  const m=new Map();
  for(const k of a) m.set(k,(m.get(k)||0)+1);
  for(const k of b){ const c=m.get(k); if(!c) return false; if(c===1) m.delete(k); else m.set(k,c-1); }
  return m.size===0;
}
function sortedRowSigs(values){ return values.map(r=>r.map(normCell).sort().join('')); }

// ─── 채점 ────────────────────────────────────────────────────────────────
function grade(probNo,userSQL){
  const ansSQL=probNo===1?ANS1:ANS2;
  if(hasRownum(userSQL)) return {ok:false,html:'<div class="verdict warn"><b>[주의] ROWNUM 감지</b><p class="mono">'+esc(ROWNUM_MSG)+'</p></div>'};
  let ur;
  try{ ur=runSQL(userSQL); }
  catch(e){ return {ok:false,html:'<div class="verdict bad"><b>[오류] 쿼리 실행 실패</b><p class="mono">'+esc(e.message)+'</p><p>쿼리를 그대로 다시 복사했는지, SQLite 문법인지 확인하세요.</p></div>'}; }
  if(!ur.length) return {ok:false,html:'<div class="verdict bad"><b>[오류] 반환된 행 없음</b><p>쿼리는 돌았지만 반환된 행이 0건입니다.</p></div>'};
  const u=ur[ur.length-1], a=runSQL(ansSQL)[0];
  const us=rowSigs(u.values), as_=rowSigs(a.values);
  const exact=multisetEq(us,as_);
  const loose=!exact && u.columns.length===a.columns.length && multisetEq(sortedRowSigs(u.values),sortedRowSigs(a.values));
  let extra='';

  if(exact||loose){
    let note=loose?'<p>값은 전부 일치합니다. 컬럼 순서만 문제와 다르니 참고하세요.</p>':'';
    if(probNo===2){
      const chk=fullCheck2(userSQL);
      if(chk && !chk.pass){
        return {ok:false,html:'<div class="verdict warn"><b>[주의] 상위 20개는 일치 — 숨은 함정 검출</b>'+note+chk.html+'</div>'};
      }
      if(chk && chk.pass) note+='<p>숨은 검증(전체 '+chk.total+'행 · 조회 0건 페이지 '+chk.zero+'개)까지 통과했습니다.</p>';
    }
    return {ok:true,html:'<div class="verdict good"><b>[정상] 정답과 일치</b> <span>('+u.values.length+'행)</span>'+note+'</div>'};
  }

  // 불일치 — 원인 힌트
  const hints=[];
  if(probNo===1){
    if(u.values.length===10&&a.values.length===12) hints.push('행수가 10입니다. <b>LIMIT 10</b> 을 쓰면 공동 10위 3명 중 일부가 잘립니다. 순위(RANK)를 매기고 "순위 ≤ 10" 으로 잘라야 합니다.');
    const flat=u.values.flat().map(String);
    if(flat.includes('남해린')) hints.push('결과에 <b>퇴직자 남해린</b>이 들어 있습니다. 재직자 필터(emp_status=\'재직\')가 빠졌거나 늦게 적용됐습니다.');
    if(u.values.length===a.values.length){
      hints.push('행수는 맞는데 값이 다릅니다. 취소건수가 전부 0이면 <b>WHERE ref_status=\'NORMAL\'</b> 로 걸어버려 취소 건이 사라진 경우입니다. 취소율 반올림(소수점 1자리)도 확인하세요.');
    }
  }else{
    const chk=fullCheck2(userSQL);
    if(chk&&!chk.pass) hints.push(chk.plain);
    if(u.columns.length!==a.columns.length) hints.push('컬럼이 '+u.columns.length+'개입니다. 문제는 7개(페이지코드·페이지명·카테고리·PV·UV·세션수·평균체류초)를 요구합니다.');
    hints.push('UV 는 비로그인(cust_no IS NULL)을 빼고 세야 합니다. COUNT(DISTINCT cust_no) 는 NULL 을 자동으로 뺍니다.');
  }
  // 차이 샘플
  const aset=new Set(as_), uset=new Set(us);
  const missing=a.values.filter((r,i)=>!uset.has(as_[i])).slice(0,3);
  const extraR=u.values.filter((r,i)=>!aset.has(us[i])).slice(0,3);
  let diff='';
  if(missing.length) diff+='<p class="dh">정답에는 있는데 내 결과에 없는 행 (일부)</p>'+tableHTML([{columns:a.columns,values:missing}],3);
  if(extraR.length) diff+='<p class="dh">내 결과에만 있는 행 (일부)</p>'+tableHTML([{columns:u.columns,values:extraR}],3);
  return {ok:false,html:'<div class="verdict bad"><b>[불일치] 정답과 다름</b> <span>내 결과 '+u.values.length+'행 / 정답 '+a.values.length+'행</span>'+
    (hints.length?'<ul>'+hints.map(h=>'<li>'+h+'</li>').join('')+'</ul>':'')+diff+'</div>'};
}

// 문제2 숨은 검증: LIMIT 을 떼고 전체 행수·PV=0 행수 확인 (정답: 988 / 376)
function fullCheck2(userSQL){
  let stripped=userSQL.replace(/;\s*$/,'')
    .replace(/FETCH\s+FIRST\s+\d+\s+ROWS?\s+ONLY\s*$/i,'')
    .replace(/LIMIT\s+\d+(\s+OFFSET\s+\d+)?\s*$/i,'');
  if(stripped===userSQL.replace(/;\s*$/,'')) return null;      // LIMIT 이 없으면 판단 불가
  let r; try{ r=runSQL(stripped); }catch(e){ return null; }
  if(!r.length) return null;
  const rows=r[r.length-1];
  const pvIdx=rows.columns.findIndex(c=>String(c).toUpperCase()==='PV');
  const total=rows.values.length;
  const zero=pvIdx<0?null:rows.values.filter(v=>Number(v[pvIdx])===0).length;
  const pass= total===988 && (zero===null||zero===376);
  let html='',plain='';
  if(!pass){
    if(total===612){
      plain='LIMIT 을 떼고 세어보면 612행입니다(정답 988행). <b>기간 조건이 WHERE 에 있어서</b> 조회 0건 페이지 376개가 통째로 사라졌습니다. LEFT JOIN 의 기간 조건은 ON 절로 옮겨야 합니다.';
    }else if(total===1000){
      plain='LIMIT 을 떼면 1,000행입니다(정답 988행). <b>폐쇄 페이지 제외 조건</b>(close_dt)이 빠졌습니다.';
    }else if(zero===0){
      plain='LIMIT 을 떼면 '+total+'행인데 PV=0 인 행이 하나도 없습니다. 0건 페이지가 사라졌거나(WHERE 함정) COUNT(*) 를 써서 0이 1로 세어졌습니다.';
    }else{
      plain='LIMIT 을 떼고 세어보면 '+total+'행입니다. 정답은 988행(그중 PV=0 이 376행)이어야 합니다.';
    }
    html='<p>'+plain+'</p>';
  }
  return {pass,total,zero,html,plain};
}

// ─── 화면: 테이블·데이터 ─────────────────────────────────────────────────
const TORDER=['employee','referral','product','branch','app_page','page_view_log'];
const TKOR={employee:'직원',referral:'가입권유 실적',product:'상품',branch:'영업점',app_page:'앱 페이지',page_view_log:'방문 로그'};
let curT='referral';

function paneData(){
  const counts={};
  TORDER.forEach(t=>counts[t]=runSQL('SELECT COUNT(*) FROM '+t)[0].values[0][0]);
  $('#p-data').innerHTML=
   '<div class="dwrap"><div class="tlist">'+
   TORDER.map(t=>'<button data-t="'+t+'" class="'+(t===curT?'on':'')+'"><span>'+TKOR[t]+'<br><small class="mono">'+t+'</small></span><i>'+counts[t].toLocaleString()+'행</i></button>').join('')+
   '</div><div class="dview"><div id="dmeta"></div><div class="dbody" id="dbody"></div></div></div>';
  $('#p-data').querySelectorAll('.tlist button').forEach(b=>b.onclick=()=>{curT=b.dataset.t;paneData();});
  showTable(curT,counts[curT]);
}
function showTable(t,total){
  const m=TABLE_META[t];
  $('#dmeta').innerHTML='<div class="dhead"><b>'+t+'</b> · '+esc(m.desc)+'<span class="r">'+total.toLocaleString()+'행 중 200행 표시</span></div>'+
   '<div class="colbar">'+m.cols.map(c=>'<span class="colchip"><b>'+c[0]+'</b> '+esc(c[1])+
     (c[2]?c[2].split(' ').map(t2=>'<i class="tag '+(t2==='PK'?'pk':t2==='IX'?'ix':'fk')+'">'+t2+'</i>').join(''):'')+'</span>').join('')+'</div>';
  $('#dbody').innerHTML=tableHTML(runSQL('SELECT * FROM '+t+' LIMIT 200'),200);
}

// ─── 화면: 문제 ──────────────────────────────────────────────────────────
function probPane(no){
  const isP1=no===1;
  const title=isP1?'문제 1 · 카드 가입권유 실적 상위 10명':'문제 2 · 앱 페이지별 조회수(PV)·방문자수(UV)';
  const ask=isP1
   ?'영업기획부: “2026년 <b>상반기 카드 추천 실적 상위 10명</b> 뽑아주세요. 이름·지점, 몇 건인지, 몇 명한테 팔았는지, 취소는 얼마나 났는지까지요.”'
   :'디지털채널부: “<b>7월 페이지별 조회수랑 방문자수</b> 좀 뽑아주세요. 프리미어 라운지랑 상품 페이지가 궁금해요. <b>아무도 안 본 페이지도</b> 봐야 해요.”';
  const reqs=isP1
   ?[['기간','2026-01-01 ~ 2026-06-30 (apply_dt)'],['대상','카드 상품(prod_type=CARD) · 재직 직원만'],
     ['실적','ref_status=NORMAL 만 인정 · 취소(CANCELLED)는 따로 센다'],
     ['순위','추천건수 기준. 동점이면 공동 순위 — <b>10위 동점자는 전부 출력</b>'],
     ['출력','순위·사번·직원명·영업점명·직급·추천건수·추천고객수·취소건수·취소율(%)']]
   :[['기간','2026-07-01 ~ 2026-07-31 (view_at)'],['대상','폐쇄 안 된 페이지 (close_dt IS NULL 또는 ≥ 2026-07-01)'],
     ['지표','PV=로그 수 · UV=고객 수(비로그인 제외) · 세션수 · 평균체류초(1자리)'],
     ['핵심','<b>조회 0건 페이지도 PV=0 으로 나와야 함</b>'],
     ['출력','PV 내림차순 상위 20 — 페이지코드·페이지명·카테고리·PV·UV·세션수·평균체류초']];
  const prompt=isP1?PROMPT1:PROMPT2;
  const pane=$(isP1?'#p-prob1':'#p-prob2');
  pane.innerHTML=
   '<div class="probs"><div class="prob">'+
   '<h3>'+title+'<span class="lv">'+(isP1?'★★★ 동점 함정':'★★★ 0건 페이지 함정')+'</span></h3>'+
   '<p class="ask">'+ask+'</p>'+
   '<table class="req">'+reqs.map(r=>'<tr><td>'+r[0]+'</td><td>'+r[1]+'</td></tr>').join('')+'</table>'+
   '<div class="steps3"><span><b>1</b> 요청문 복사</span><span>→</span><span><b>2</b> AI가 쿼리 작성</span><span>→</span><span><b>3</b> 붙여넣고 실행＋채점</span></div>'+
   '<div class="bar"><button class="ghost" id="copy'+no+'">AI 요청문 복사 (F2)</button><span id="copied'+no+'" class="copied"></span></div>'+
   '<textarea id="sql'+no+'" spellcheck="false" placeholder="-- AI가 만들어준 쿼리를 여기 붙여넣으세요"></textarea>'+
   '<div class="bar"><button class="run" id="run'+no+'">실행＋채점 (F8)</button>'+
   '<button class="ghost" id="clr'+no+'">지우기 (F4)</button><span class="stat" id="stat'+no+'"></span></div>'+
   '<div id="verdict'+no+'"></div>'+
   '<div class="out" id="out'+no+'" style="min-height:120px;max-height:420px"></div>'+
   '<details><summary>정답 쿼리 보기 (채점 뒤에 여세요)</summary><div class="body"><pre class="sql">'+esc(isP1?ANS1:ANS2)+'</pre>'+
   (isP1?'<div class="trap"><b>함정 요약</b> — ① “상위 10명”을 LIMIT 10(Oracle: FETCH FIRST 10 ROWS ONLY)으로 자르면 공동 10위 3명 중 1명이 잘립니다(정답은 12행). ② 재직 필터를 빼면 퇴직자 남해린이 3위에 끼어듭니다. ③ WHERE 로 NORMAL 만 남기면 취소건수를 셀 수 없습니다.</div>'
        :'<div class="trap"><b>함정 요약</b> — ① LEFT JOIN 의 기간 조건을 WHERE 에 두면 조회 0건 페이지 376개가 사라집니다(988→612행). 상위 20개는 똑같이 나와서 눈으로는 못 잡습니다 — 그래서 채점기가 LIMIT 을 떼고 전체 행수까지 확인합니다. ② COUNT(*) 를 쓰면 0건 페이지가 PV=1 로 나옵니다.</div>')+
   '</div></details></div></div>';
  $('#copy'+no).onclick=()=>{copyText(prompt);$('#copied'+no).textContent='복사됨 — AI 채팅창에 붙여넣으세요';setTimeout(()=>$('#copied'+no).textContent='',4000);};
  $('#clr'+no).onclick=()=>{$('#sql'+no).value='';$('#verdict'+no).innerHTML='';$('#out'+no).innerHTML='';$('#stat'+no).textContent='';};
  $('#run'+no).onclick=()=>runProb(no);
  $('#sql'+no).addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();runProb(no);}});
}
function runProb(no){
  const sql=$('#sql'+no).value.trim();
  if(!sql){$('#verdict'+no).innerHTML='<div class="verdict warn"><b>[안내] 쿼리를 붙여넣어 주세요</b></div>';return;}
  const t0=performance.now();
  const g=grade(no,sql);
  $('#verdict'+no).innerHTML=g.html;
  try{
    const r=runSQL(sql);
    $('#out'+no).innerHTML=tableHTML(r,100);
    const last=r.length?r[r.length-1].values.length:0;
    $('#stat'+no).textContent=last.toLocaleString()+'행 · '+(performance.now()-t0).toFixed(0)+' ms';
  }catch(e){ $('#out'+no).innerHTML=''; $('#stat'+no).textContent=''; }
}
function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).catch(()=>fallbackCopy(t));}
  else fallbackCopy(t);
}
function fallbackCopy(t){const ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}ta.remove();}

// ─── 화면: 자유 쿼리 ─────────────────────────────────────────────────────
const FREE=[
 ['추천건수 많은 직원 TOP 5',"SELECT e.emp_nm AS 직원명, b.branch_nm AS 지점, COUNT(*) AS 추천건수\nFROM referral r\nJOIN employee e ON e.emp_no=r.ref_emp_no\nJOIN branch b ON b.branch_cd=e.branch_cd\nWHERE r.ref_status='NORMAL'\nGROUP BY e.emp_nm, b.branch_nm\nORDER BY 추천건수 DESC\nLIMIT 5;"],
 ['카드 상품별 가입 건수',"SELECT p.prod_nm AS 상품명, COUNT(*) AS 가입건수\nFROM referral r JOIN product p ON p.prod_cd=r.prod_cd\nWHERE p.prod_type='CARD' AND r.ref_status='NORMAL'\nGROUP BY p.prod_nm ORDER BY 가입건수 DESC;"],
 ['채널별 실적 비중',"SELECT channel AS 채널, COUNT(*) AS 건수\nFROM referral WHERE ref_status='NORMAL'\nGROUP BY channel ORDER BY 건수 DESC;"],
 ['많이 본 페이지 TOP 10',"SELECT p.page_nm AS 페이지, COUNT(*) AS 조회수\nFROM page_view_log l JOIN app_page p ON p.page_id=l.page_id\nGROUP BY p.page_nm ORDER BY 조회수 DESC LIMIT 10;"],
 ['기기별 방문 수',"SELECT device AS 기기, COUNT(*) AS 방문수, COUNT(DISTINCT cust_no) AS 방문고객수\nFROM page_view_log GROUP BY device ORDER BY 방문수 DESC;"]];

function paneFree(){
  $('#p-free').innerHTML='<div class="qwrap">'+
   '<div class="chips">'+FREE.map((f,i)=>'<button data-i="'+i+'">'+f[0]+'</button>').join('')+'</div>'+
   '<textarea id="fsql" spellcheck="false">-- 자유롭게 조회해 보세요 (Ctrl+Enter 실행)\nSELECT prod_nm AS 상품명, prod_type AS 유형 FROM product ORDER BY prod_type;</textarea>'+
   '<div class="bar"><button class="run" id="frun">실행 (F8)</button><span class="stat" id="fstat"></span></div>'+
   '<div class="out" id="fout"></div></div>';
  $('#p-free').querySelectorAll('.chips button').forEach(b=>b.onclick=()=>{$('#fsql').value=FREE[b.dataset.i][1];freeRun();});
  $('#frun').onclick=freeRun;
  $('#fsql').addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();freeRun();}});
}
function freeRun(){
  const t0=performance.now();
  if(hasRownum($('#fsql').value)){ $('#fout').innerHTML='<div class="msg err">'+esc(ROWNUM_MSG)+'</div>'; $('#fstat').textContent=''; return; }
  try{
    const r=runSQL($('#fsql').value);
    $('#fout').innerHTML=tableHTML(r,500);
    $('#fstat').textContent=(r.length?r[r.length-1].values.length.toLocaleString():'0')+'행 · '+(performance.now()-t0).toFixed(0)+' ms';
  }catch(e){ $('#fout').innerHTML='<div class="msg err">✕ '+esc(e.message)+'</div>'; $('#fstat').textContent=''; }
}

// ─── 탭 & 초기화 ─────────────────────────────────────────────────────────
document.addEventListener('keydown',e=>{
  const on=document.querySelector('.pane.on');
  if(e.key==='F8'){ e.preventDefault();
    if(on&&on.id==='p-prob1') runProb(1); else if(on&&on.id==='p-prob2') runProb(2);
    else if(on&&on.id==='p-free') freeRun(); }
  if(e.key==='F2'){ e.preventDefault();
    if(on&&on.id==='p-prob1') document.querySelector('#copy1')?.click();
    if(on&&on.id==='p-prob2') document.querySelector('#copy2')?.click(); }
  if(e.key==='F4'){ e.preventDefault();
    if(on&&on.id==='p-prob1') document.querySelector('#clr1')?.click();
    if(on&&on.id==='p-prob2') document.querySelector('#clr2')?.click(); }
});
document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
    document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('on',x===b));
    document.querySelectorAll('.pane').forEach(p=>p.classList.remove('on'));
    $('#p-'+b.dataset.p).classList.add('on');
  });
  function b64u8(s){const b=atob(s);const u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u;}
  initSqlJs({wasmBinary:b64u8(WASM_B64)}).then(SQL=>{
    db=buildDB(SQL); registerCompat(db);
    paneData(); probPane(1); probPane(2); paneFree();
  }).catch(e=>{ $('#p-data').innerHTML='<div class="msg err">엔진 초기화 실패: '+esc(e)+'</div>'; });
});
