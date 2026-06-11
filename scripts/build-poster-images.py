# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
W, DEFAULT_H = 1080, 2160
FONT = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
FONT_FALLBACK = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'

BLUE=(0,102,204); BLUE2=(37,99,235); CYAN=(14,165,233); NAVY=(15,23,42); DARK=(28,34,45)
TEXT=(17,24,39); MUTED=(88,99,116); LINE=(220,229,241); SOFT=(246,249,255); WHITE=(255,255,255)
GREEN=(22,163,74); RED=(239,68,68); ORANGE=(234,88,12)

def font(size:int, weight='regular'):
    # AppleSDGothic TTC exposes a good Korean face at index 0; use fallback if needed.
    try:
        return ImageFont.truetype(FONT, size=size, index=0)
    except Exception:
        return ImageFont.truetype(FONT_FALLBACK, size=size)

def canvas(dark=False, height=DEFAULT_H):
    img=Image.new('RGB',(W,height),(255,255,255))
    px=img.load()
    for y in range(height):
        t=y/(height-1)
        if dark:
            c=tuple(int((20,26,36)[i]*(1-t)+(38,43,52)[i]*t) for i in range(3))
        else:
            c=tuple(int((255,255,255)[i]*(1-t)+(244,248,255)[i]*t) for i in range(3))
        for x in range(W): px[x,y]=c
    d=ImageDraw.Draw(img,'RGBA')
    d.ellipse((-160,-120,520,520), fill=(37,99,235,36 if dark else 26))
    d.ellipse((760,-180,1260,350), fill=(14,165,233,22 if dark else 18))
    return img

def rounded(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def shadow_box(img, xy, r=24, fill=WHITE, outline=LINE, shadow=(15,23,42,24), offset=(0,12), blur=24):
    layer=Image.new('RGBA', img.size, (0,0,0,0)); ld=ImageDraw.Draw(layer,'RGBA')
    sx=(xy[0]+offset[0], xy[1]+offset[1], xy[2]+offset[0], xy[3]+offset[1])
    ld.rounded_rectangle(sx, radius=r, fill=shadow)
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)) if img.mode=='RGBA' else layer.filter(ImageFilter.GaussianBlur(blur)))
    d=ImageDraw.Draw(img,'RGBA'); d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=1)

def text_size(draw, text, f):
    b=draw.textbbox((0,0), text, font=f)
    return b[2]-b[0], b[3]-b[1]

def wrap(draw, text, f, max_w):
    lines=[]
    for para in str(text).split('\n'):
        cur=''
        for ch in para:
            test=cur+ch
            if draw.textlength(test, font=f) <= max_w or not cur:
                cur=test
            else:
                lines.append(cur); cur=ch
        lines.append(cur)
    return lines

def draw_text(draw, xy, text, f, fill=TEXT, max_w=None, line_gap=6, anchor=None, align='left'):
    x,y=xy
    if max_w is None:
        draw.text((x,y), text, font=f, fill=fill, anchor=anchor)
        return y + text_size(draw,text,f)[1]
    lines=wrap(draw, text, f, max_w)
    line_h=text_size(draw,'가나다ABC',f)[1]+line_gap
    for line in lines:
        tx=x
        if align=='center':
            tx=x+max_w/2; draw.text((tx,y), line, font=f, fill=fill, anchor='ma')
        else:
            draw.text((tx,y), line, font=f, fill=fill)
        y += line_h
    return y

def paste_fit(base, path, box, mode='contain', radius=18, bg=(255,255,255)):
    src=Image.open(path).convert('RGB')
    bw,bh=box[2]-box[0], box[3]-box[1]
    sw,sh=src.size
    scale=max(bw/sw,bh/sh) if mode=='cover' else min(bw/sw,bh/sh)
    nw,nh=max(1,int(sw*scale)),max(1,int(sh*scale))
    src=src.resize((nw,nh), Image.Resampling.LANCZOS)
    if mode=='cover':
        left=max(0,(nw-bw)//2); top=max(0,(nh-bh)//2); src=src.crop((left,top,left+bw,top+bh))
    else:
        bgim=Image.new('RGB',(bw,bh),bg); bgim.paste(src,((bw-nw)//2,(bh-nh)//2)); src=bgim
    mask=Image.new('L',(bw,bh),0); md=ImageDraw.Draw(mask); md.rounded_rectangle((0,0,bw,bh),radius=radius,fill=255)
    base.paste(src,(box[0],box[1]),mask)

def header(d, title, subtitle, page, dark=False):
    d.text((58,52), subtitle.upper(), font=font(19), fill=(139,193,255) if dark else BLUE)
    d.text((58,84), title, font=font(72), fill=WHITE if dark else TEXT)
    d.text((1018,46), f'{page:02d}', font=font(62), fill=(147,197,253,55) if dark else (0,102,204,38), anchor='ra')

def card(img, xy, title, body, icon=None, dark=False, title_color=None, body_size=18):
    d=ImageDraw.Draw(img,'RGBA')
    fill=(255,255,255,235)
    outline=(223,231,242,255) if not dark else (191,219,254,160)
    shadow_box(img, xy, 22, fill, outline, shadow=(15,23,42,18 if not dark else 0))
    x,y=xy[0]+22, xy[1]+20
    if icon:
        d.text((x,y), icon, font=font(26), fill=title_color or (WHITE if dark else BLUE)); x+=40
    d.text((x,y), title, font=font(25), fill=title_color or TEXT)
    draw_text(d,(xy[0]+22,y+36),body,font(body_size),fill=MUTED,max_w=xy[2]-xy[0]-44,line_gap=5)

def footer(d, page, dark=False, height=DEFAULT_H, left_text='신한은행 TECH혁신Unit 개발 AX Cell'):
    fill=(160,180,210) if dark else (112,129,151)
    d.text((58,height-44),left_text,font=font(15),fill=fill)
    d.text((W-58,height-44),f'Poster {page}/3',font=font(15),fill=fill,anchor='ra')

def page1():
    H1=2820
    img=canvas(True,H1).convert('RGBA'); d=ImageDraw.Draw(img,'RGBA')
    header(d,'택가이코드','TECHAI CODE · INTERNAL AI CODING AGENT',1,True)
    d.text((58,178),'터미널과 VS Code에서 쓰는\n사내 AI 개발 에이전트',font=font(36),fill=(218,230,255))
    paste_fit(img,ASSETS/'techai_tui_icon.png',(58,292,150,384),radius=24,bg=(15,23,42))
    d.text((166,292),'TECHAI',font=font(54),fill=WHITE); d.text((166,342),'CODE',font=font(54),fill=(139,190,255))
    chips=['Terminal','VS Code Extension','Same Engine','On-Premise']
    cx, cy = 58, 414
    chip_f = font(15)
    for ch in chips:
        tw=d.textlength(ch,font=chip_f)
        if cx + tw + 30 > 430:
            cx, cy = 58, cy + 48
        rounded(d,(cx,cy,cx+tw+30,cy+40),20,(255,255,255,235),(255,255,255,80))
        d.text((cx+15,cy+10),ch,font=chip_f,fill=(30,41,59))
        cx+=tw+42
    rounded(d,(58,526,430,574),24,(37,99,235,210),(125,211,252,120)); d.text((78,540),'LIVE URL',font=font(13),fill=(191,219,254)); d.text((174,537),'techaicode.vercel.app',font=font(21),fill=WHITE)
    shadow_box(img,(548,170,1020,542),28,(10,16,30,245),(80,110,160,80),shadow=(0,0,0,80)); paste_fit(img,ASSETS/'techaicode_terminal.png',(566,190,1002,522),radius=18,bg=(10,16,30))
    d.text((58,586),'무엇이 다른가',font=font(48),fill=WHITE)
    shadow_box(img,(58,654,504,846),24,(239,246,255,245),(191,219,254,160),shadow=(0,0,0,40)); d.text((86,682),'웹 챗봇이 아니라',font=font(30),fill=TEXT); d.text((86,724),'코드베이스 안에서 실제로 작업',font=font(30),fill=BLUE); draw_text(d,(86,774),'프로젝트를 읽고 파일·Shell·git 도구를 호출하며, 수정과 검증 루프까지 이어갑니다.',font(19),fill=MUTED,max_w=372)
    list_items=['파일 검색·읽기·수정','Shell 명령과 git 흐름 지원','터미널 버전과 VS Code Extension이 같은 엔진 사용','API Key와 로그로 관리 가능']
    y=660
    for it in list_items:
        rounded(d,(532,y,1020,y+42),16,(255,255,255,238),(191,219,254,160))
        d.text((552,y+9),'→',font=font(20),fill=BLUE2)
        d.text((584,y+9),it,font=font(20),fill=(30,41,59))
        y+=51
    d.text((58,900),'택가이 플랫폼 구조',font=font(44),fill=WHITE)
    shadow_box(img,(58,962,1020,1320),24,(255,255,255,245),(207,224,247,255),shadow=(0,0,0,65)); paste_fit(img,ASSETS/'techai_platform_map_complete.png',(76,980,1002,1302),radius=16,bg=WHITE)
    d.text((58,1360),'택가이Web은 중앙 관리 통로',font=font(42),fill=WHITE)
    d.text((58,1410),'사내 SSO, 사용자 포털, 관리자 페이지와 API Key 관리까지 이어지는 실제 운영 화면입니다.',font=font(21),fill=(207,222,242))
    shadow_box(img,(58,1466,1020,2066),26,(255,255,255,245),(207,224,247,255),shadow=(0,0,0,54)); paste_fit(img,ASSETS/'tweb_screen.png',(84,1494,994,2038),radius=18,bg=WHITE)
    cards=[('SSO 로그인','사내 스윙 SSO와 사번 기반 사용자 식별'),('사용량 측정','부서별·개인별·모델별 요청/토큰 집계'),('메시지·오류 로깅','요청/응답 메타데이터, 오류, 재시도 내역 확인'),('API Key 발급','개인별 모델 권한과 사용량 추적 관리')]
    positions=[(58,2118,504,2276),(532,2118,1020,2276),(58,2310,504,2468),(532,2310,1020,2468)]
    for pos,(t,b) in zip(positions,cards): card(img,pos,t,b,dark=True,body_size=17)
    footer(d,1,True,H1); return img.convert('RGB')

def page2():
    H2=3800
    img=canvas(False,H2).convert('RGBA'); d=ImageDraw.Draw(img,'RGBA')
    header(d,'제품 · 성능 · POC','PRODUCT · MODEL · USE CASE',2,False)
    d.text((58,176),'택가이코드는 개발자가 실제로 쓰는 제품입니다',font=font(42),fill=TEXT)
    d.text((58,226),'Terminal과 VS Code Extension, 두 제품 모두 같은 엔진을 씁니다.',font=font(25),fill=MUTED)
    shadow_box(img,(58,286,510,626),26,(11,16,32,255),(51,65,85,255),shadow=(15,23,42,45)); paste_fit(img,ASSETS/'techaicode_terminal.png',(78,306,490,606),radius=16,bg=(11,16,32))
    card(img,(538,286,780,440),'Terminal Agent','프로젝트 루트에서 바로 실행. 파일·셸·git 작업과 연결됩니다.',body_size=16)
    card(img,(804,286,1020,440),'VS Code Extension','에디터 안에서 같은 엔진과 도구 실행 루프를 사용합니다.',body_size=16)
    card(img,(538,466,780,626),'Same Engine','모델 권한, 로그, API Key 관리 체계는 동일합니다.',body_size=16)
    card(img,(804,466,1020,626),'오픈소스 대비 경쟁력','모델 성능뿐 아니라 코드 어시스턴트 도구 자체도 기존 오픈소스 도구보다 오히려 경량화되며 높은 성능을 보여줍니다.',body_size=14)

    d.text((58,696),'앞선 영상은 이미 4월 제품이고, 지금은 2배 이상 더 좋아졌습니다',font=font(34),fill=TEXT)
    shadow_box(img,(58,756,512,1158),24,WHITE,LINE,shadow=(15,23,42,22))
    d.text((86,782),'코딩 Agent 생산성',font=font(28),fill=TEXT); d.text((86,820),'프론티어=100 상대지수 · 현재 적용 모델 하이라이트',font=font(16),fill=MUTED)
    bars=[('GPT-5.5 / Codex',100,BLUE2),('Claude Opus 4.8',97,CYAN),('코딩모델 35B',87,GREEN),('코딩모델 30B',83,(122,135,151)),('범용모델 120B',80,(122,135,151))]
    y=870
    for name,val,col in bars:
        if name=='코딩모델 35B': rounded(d,(74,y-8,496,y+43),17,(255,241,242,255),RED,3)
        d.text((86,y),name,font=font(17),fill=(153,27,27) if name=='코딩모델 35B' else TEXT)
        rounded(d,(230,y+3,440,y+25),11,(234,240,248,255),None)
        rounded(d,(230,y+3,230+int(210*val/100),y+25),11,col,None)
        d.text((456,y),str(val),font=font(18),fill=TEXT)
        y+=50
    draw_text(d,(86,1110),'모델 자체보다 Agent Loop, Tool Calling, Repository Reasoning, 한국어 요구사항 처리 차이가 실제 생산성에 크게 반영됩니다.',font(14),fill=MUTED,max_w=386,line_gap=3)
    shadow_box(img,(540,756,1020,1158),24,(239,246,255,255),(191,219,254,255),shadow=(15,23,42,22))
    d.text((568,792),'도구 자체도 가볍고 빠르게',font=font(30),fill=TEXT)
    draw_text(d,(568,846),'기존 오픈소스 도구보다 경량화된 구조로, 내부망에서도 높은 반응성과 안정적인 작업 루프를 목표로 합니다.',font(20),fill=MUTED,max_w=400,line_gap=7)
    rounded(d,(568,1038,788,1084),23,(255,255,255,255),(191,219,254,255)); d.text((678,1050),'경량화',font=font(18),fill=BLUE2,anchor='ma')
    rounded(d,(810,1038,994,1084),23,(255,255,255,255),(191,219,254,255)); d.text((902,1050),'고성능',font=font(18),fill=BLUE2,anchor='ma')

    d.text((58,1236),'택가이코드 VS Code Extension',font=font(42),fill=TEXT)
    d.text((58,1288),'에디터 안에서 프로젝트 맥락을 읽고, 같은 엔진으로 파일·검색·Shell 작업을 이어갑니다.',font=font(22),fill=MUTED)
    shadow_box(img,(58,1342,1020,1868),26,WHITE,LINE,shadow=(15,23,42,28)); paste_fit(img,ASSETS/'techaicode_vscode.png',(84,1380,994,1828),radius=18,bg=WHITE)

    d.text((58,1948),'현재 개발중인 “택가이 데스크톱”',font=font(42),fill=TEXT)
    d.text((58,2000),'개발과 단순 AI 질문 기능을 넘어, 대부분의 개인화 에이전트를 대체할 방향입니다.',font=font(23),fill=BLUE)
    shadow_box(img,(58,2058,1020,2628),26,WHITE,LINE,shadow=(15,23,42,28)); paste_fit(img,ASSETS/'techaicode_desktop_app.png',(84,2088,994,2598),radius=18,bg=WHITE)
    shadow_box(img,(58,2678,1020,2868),24,(239,246,255,255),(191,219,254,255),shadow=(15,23,42,22))
    d.text((86,2708),'택가이 데스크톱 확장 방향',font=font(30),fill=BLUE)
    draw_text(d,(86,2754),'업무망 사용 확대, 문서작성·스케줄관리, 사용자 개인화·내장 DB를 통해 일반 업무 환경으로 확장합니다. 개발과 단순 AI 질문 기능을 넘어 대부분의 개인화 에이전트를 대체할 것입니다.',font(22),fill=TEXT,max_w=880,line_gap=8)
    chips=[('업무망 확대',86),('문서작성',260),('스케줄관리',414),('개인화 DB',594),('개인화 에이전트 대체',760)]
    for label,x in chips:
        tw=d.textlength(label,font=font(16))
        rounded(d,(x,2820,x+tw+30,2858),19,(255,255,255,255),(191,219,254,255))
        d.text((x+15,2829),label,font=font(16),fill=BLUE2)

    d.text((58,2948),'땡겨요 POC에서 확인한 가치',font=font(38),fill=TEXT)
    poc=[('화면 파악','기존 화면과 요구사항 정리'),('구조 분석','React 프로젝트 흐름 파악'),('코드 수정','회원가입·검색·주문 플로우 구현')]
    x=58
    for t,b in poc:
        card(img,(x,3004,x+300,3134),t,b,body_size=15,title_color=BLUE); x+=326
    shadow_box(img,(58,3168,512,3274),20,(239,246,255,255),(191,219,254,255)); d.text((84,3192),'“비숙련자 진입장벽 낮춤”',font=font(22),fill=BLUE); draw_text(d,(84,3226),'복잡한 프로젝트 구조도 AI 도움으로 빠르게 화면과 흐름을 이해',font(15),fill=MUTED,max_w=398)
    shadow_box(img,(540,3168,1020,3274),20,(239,246,255,255),(191,219,254,255)); d.text((566,3192),'“완벽히 동작하는 비즈니스 화면 코드”',font=font(21),fill=BLUE); draw_text(d,(566,3226),'단순 목업이 아니라 실제 업무 플로우에 맞춰 동작하는 화면 코드까지 구현',font(15),fill=MUTED,max_w=424)
    footer(d,2,False,H2); return img.convert('RGB')

def page3():
    img=canvas(False).convert('RGBA'); d=ImageDraw.Draw(img,'RGBA')
    header(d,'실제 후기 · 확산 · 운영 지표','REAL FEEDBACK · ADOPTION · OPERATION METRICS',3,False)
    reviews=[('김지은 프로','디지털서비스개발부 · React','내부망 AI임에도 똑똑한 택가이코드 덕분에 업무효율이 매우 늘었습니다.'),('노태경 프로','투자서비스개발부 · Proframe 5','사이즈가 큰 프로젝트에서도 끊기지 않고 수행되어 너무 좋습니다.'),('이승민 프로','디지털서비스개발부 · SOL APP','업무 진행하면서 많은 도움이 되었습니다. 주기적인 업데이트 부탁드립니다!'),('김예진 프로','디지털서비스개발부 · SOL APP 뱅킹','AI와 함께 답변을 도출했을 때 개발속도와 결과물이 더 빨랐습니다.'),('변은서 프로','디지털서비스개발부 · PB·공과금','정보 검색 시간이 단축되어 업무를 빨리 끝낼 수 있어 도움이 됩니다.'),('서문교 프로','디지털서비스개발부 · 이벤트개발','단순 반복 개발건 70% 시간단축, 만족도 5점에 5점입니다.'),('김장원 팀장','글로벌서비스개발부','내부망 환경에서도 AI Coding Agent가 실제 활용될 수 있다는 점에 놀라웠습니다.'),('김혜민 프로','땡겨요사업단 · 플랫폼운영 Cell','사내망 보안 환경에서도 최고 수준 AI 개발 툴을 자체 테스트한 큰 의미가 있었습니다.'),('정다윤 프로','정보서비스개발부 · CXM Cell','IDE 내 오류 검증, 복잡한 쿼리/쉘 학습, 기술 내용 요약에 큰 도움이 됩니다.')]
    x0,y0=58,166; cw,ch=302,158; gap=16
    for idx,(name,dept,body) in enumerate(reviews):
        x=x0+(idx%3)*(cw+gap); y=y0+(idx//3)*(ch+gap)
        shadow_box(img,(x,y,x+cw,y+ch),20,WHITE,LINE,shadow=(15,23,42,16)); d.text((x+18,y+16),dept,font=font(12),fill=MUTED); d.text((x+18,y+42),name,font=font(23),fill=BLUE); draw_text(d,(x+18,y+78),'“'+body+'”',font(14),fill=TEXT,max_w=cw-36,line_gap=3)
    y=692
    card(img,(58,y,360,y+126),'외부개발자 온보딩','처음 보는 코드베이스를 혼자 파악하는 시간을 줄입니다.',body_size=16)
    card(img,(388,y,690,y+126),'추가 사용문의 부서','고객상담센터 · Data플랫폼Unit · 고객경험혁신센터',body_size=16)
    card(img,(718,y,1020,y+126),'운영 가능 구조','API Key, 로그, 사용량, 오류 이력으로 통제 가능한 AI 동료.',body_size=16)
    d.text((58,874),'2026년 6월 기준 택가이 주간 운영지표',font=font(42),fill=TEXT); d.text((58,928),'5영업일 기준 · 실제 운영 통계',font=font(20),fill=MUTED)
    metrics=[('전체 사용자','1,125명+','개발망 852명+ / 업무망 273명+'),('주간 활성 사용자','510명+','개발망 429명+ / 업무망 81명+'),('API Key 발급 개발자','236명+','개발망에서 개인 Key 발급 후 사용'),('하루 평균 요청','4,500+','일 평균 요청 횟수')]
    x=58
    for t,v,s in metrics:
        shadow_box(img,(x,974,x+222,1138),20,WHITE,LINE,shadow=(15,23,42,16)); d.text((x+18,998),t,font=font(17),fill=MUTED); d.text((x+18,1034),v,font=font(38),fill=BLUE2); draw_text(d,(x+18,1090),s,font(13),fill=MUTED,max_w=186,line_gap=2); x+=246
    shadow_box(img,(58,1170,430,1398),24,(9,35,92,255),(37,99,235,255),shadow=(15,23,42,32));
    d.pieslice((82,1212,202,1332),-90,234,fill=GREEN); d.pieslice((82,1212,202,1332),234,270,fill=(229,238,251)); d.ellipse((112,1242,172,1302),fill=WHITE); d.text((142,1260),'90%',font=font(22),fill=GREEN,anchor='mm')
    d.text((228,1210),'개발망 주간 토큰 / 택가이코드 비중',font=font(17),fill=(210,226,255)); d.text((228,1248),'8.09억+',font=font(48),fill=WHITE); draw_text(d,(228,1310),'5영업일 기준 809,242,813 tokens · 총 토큰 사용량의 90%가 택가이코드에서 발생',font(14),fill=(219,234,254),max_w=170,line_gap=3)
    shadow_box(img,(458,1170,1020,1546),24,WHITE,LINE,shadow=(15,23,42,16)); d.text((486,1196),'부서별 주간 사용량 TOP 10',font=font(28),fill=TEXT)
    depts=[('신한은행 외부개발팀',237.9,100),('글로벌서비스개발부',169.7,71),('ICT아웃소싱베트남',150.1,63),('디지털서비스개발부',82.8,35),('정보서비스개발부',47.8,20),('Data플랫폼Unit',44.7,19),('Tech운영부',42.5,18),('투자서비스개발부',17.2,8),('DS개발팀',13.9,6),('금융서비스개발부',8.3,4)]
    yy=1244
    for i,(name,m,pct) in enumerate(depts,1):
        d.text((486,yy+3),str(i),font=font(14),fill=MUTED); rounded(d,(516,yy,908,yy+22),11,(234,240,248),None); rounded(d,(516,yy,516+int(392*pct/100),yy+22),11,(37,99,235),None); d.text((526,yy+2),name,font=font(12),fill=WHITE); d.text((928,yy+1),f'{m:.1f}M',font=font(14),fill=TEXT); yy+=28
    draw_text(d,(486,1520),'그 외 Tech기획부·여신서비스개발부·AI개발부 등 사용 중 · 다음 순위 5.7M+ · 막대는 1위 대비',font(13),fill=MUTED,max_w=500,line_gap=2)
    shadow_box(img,(58,1594,1020,1814),28,(17,24,39,255),(51,65,85,255),shadow=(15,23,42,30));
    draw_text(d,(104,1630),'택가이코드는 오픈소스 모델만으로 사내 온프레미스 환경에서 이용 가능하며, 내부망 환경에서 외부솔루션과 오픈소스보다 오히려 뛰어난 AI 코드 어시스턴트입니다.',font(30),fill=WHITE,max_w=872,line_gap=8,align='center')
    rounded(d,(350,1750,730,1798),24,WHITE,None); d.text((540,1762),'techaicode.vercel.app · PDF / Poster',font=font(16),fill=TEXT,anchor='ma')
    footer(d,3,False,left_text='신한은행 TECH혁신Unit 개발 AX Cell · 담당자: 김지원프로 · 이성렬프로'); return img.convert('RGB')

def main():
    pages=[page1(),page2(),page3()]
    outs=[]
    for i,p in enumerate(pages,1):
        out=ASSETS/f'techaicode_poster_page_{i:02d}.png'
        p.save(out,optimize=True)
        print(out.relative_to(ROOT), p.size)
        outs.append(out)
    pdf=ASSETS/'techaicode_poster.pdf'
    try:
        import fitz
        doc=fitz.open()
        for out in outs:
            with Image.open(out) as im:
                iw, ih = im.size
            rect=fitz.Rect(0,0,iw,ih)
            page=doc.new_page(width=iw,height=ih)
            page.insert_image(rect,filename=str(out),keep_proportion=False)
        doc.save(pdf,deflate=True,garbage=4)
        doc.close()
    except Exception:
        imgs=[Image.open(p).convert('RGB') for p in outs]
        imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=144)
    print(pdf.relative_to(ROOT), round(pdf.stat().st_size/1024/1024,2),'MB')
if __name__=='__main__': main()
