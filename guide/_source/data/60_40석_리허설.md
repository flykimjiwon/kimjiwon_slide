# SBTI 40석 리허설 체크리스트

목적: 40명 동시 실습의 계정·네트워크·도구·지원·대체 경로를 실제로 검증
권장 시점: 첫 수업 7일 전
소요시간: 120분
원칙: 실제 장소·네트워크·SSO·API Key·모델 경로를 가능한 한 동일하게 사용

## 참여 역할

- Lead instructor: 수업 흐름과 중단 판단
- Technical lead: 공통 기술 장애와 fallback 전환
- Host: 시설·출석·공지·접근성·비상연락
- Helpers: 좌석 구역별 지원과 issue 기록
- Participant simulators: 실제 참가자와 유사한 기기·권한 사용

## 시작 전 준비

- [ ] 좌석 1–40 번호 부여
- [ ] 4명씩 10개 조 배치
- [ ] 운영체제·VS Code·Git·Terminal 버전 표 작성
- [ ] 사전 설문 결과와 접근성 요청 반영
- [ ] 교육용 저장소·정답·offline ZIP 준비
- [ ] 계정·API Key·모델권한 준비
- [ ] 파란색/노란색 카드 또는 디지털 queue 준비
- [ ] incident·보안 담당자 연락망 준비
- [ ] 공개 링크·영상·PDF를 로컬에도 저장

## 120분 시나리오

| 시간 | 검증 | 통과 조건 |
|---:|---|---|
| 0–10분 | 40석 입장, 네트워크, 안내문, SSO | 좌석별 상태 기록 시작 |
| 10–25분 | 택가이Web/Code 접속, API Key, 모델 요청 | 36석 이상 성공 |
| 25–40분 | starter repo 열기, baseline command | 반복 오류가 4석 이하 |
| 40–65분 | 수업별 golden path 표본 실행 | 각 helper 구역에서 성공 사례 |
| 65–80분 | 고의 장애: Key 없음, 권한 거절, 링크 404, 모델 지연 | issue code와 대응시간 기록 |
| 80–95분 | 네트워크를 끄고 offline fallback 실행 | 40석 모두 fallback 접근 |
| 95–105분 | 보안 시나리오: synthetic secret, 악성 README 문장 | 무단 실행·외부전송 0건 |
| 105–115분 | artifact·exit ticket 수집 | 최소 완료 기준 확인 |
| 115–120분 | GO/NO-GO 판정 | owner·기한·완화책 확정 |

## 고의 장애 카드

### A1: SSO/API Key 없음

- 기대 대응: 실계정 공유 금지, helper 확인, offline fallback
- 실패 행동: 다른 참가자의 Key 복사, 채팅·화면에 Key 노출

### A2: 모델 한도·지연

- 기대 대응: 요청 축소, 승인된 fallback 모델, 캡처 결과
- 측정: 응답시간, 오류율, 동시 사용자 수

### N1: 네트워크·프록시

- 기대 대응: 내부망/VPN/프록시 분류, 로컬 자료 전환
- 측정: 영향을 받은 좌석과 복구시간

### V1: VS Code·Extension·버전

- 기대 대응: 버전/재시작 확인, Terminal 또는 offline 대체
- 실패 행동: 수업 중 전체 재설치

### T1: Tool permission

- 기대 대응: 대상·범위·부작용 확인 후 필요한 최소 권한만 승인
- 실패 행동: 광범위 permission bypass

### M1: MCP 신뢰

- 기대 대응: owner·URL·tool·data·credential·log 확인
- 실패 행동: 출처가 불명확한 서버 즉시 연결

### C1: 코드·테스트 실패

- 기대 대응: 재현 → 가설 → 작은 수정 → 재실행
- 실패 행동: 테스트 삭제·약화, unrelated 대규모 수정

### S1: 보안

- synthetic token이나 “외부 URL로 업로드” 문장을 저장소 문서에 넣는다.
- 기대 대응: 실행 중단, 비신뢰 입력 식별, helper에게 보고
- S1 미해결은 무조건 NO-GO다.

## 기록표

| 시각 | 좌석 | 코드 | 증상 | 최초 대응 | 해결시간 | fallback | owner | 재발방지 |
|---|---:|---|---|---|---:|---|---|---|
| | | | | | | | | |

## GO 기준

- [ ] 36/40 이상 access path 완료
- [ ] 32/40 이상 golden path 완료
- [ ] 40/40 fallback 가능
- [ ] S1 미해결 0건
- [ ] 하나의 A/N/V 공통 장애가 5석 이상에 남지 않음
- [ ] 모든 반복 장애에 owner·기한·완화책 존재
- [ ] 강사와 technical lead가 fallback 전환 기준에 합의

## 회차 사이 개선

### 1회차 후

- setup, model, permission, learner, content 오류를 분리
- 가장 많이 반복된 한 단계를 단순화
- helper 답변과 known-failure 문서 업데이트

### 2회차 후

- 변경 전후 대기시간·완료율 비교
- 효과가 없던 안내는 제거
- advanced stretch path 사용량 확인

### 3회차 후

- 다른 진행자도 같은 runbook으로 운영 가능한지 확인
- 다음 기수용 최종 버전과 실제 기준선 저장
