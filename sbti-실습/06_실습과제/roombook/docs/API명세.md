# roombook API 명세 (v2)

Base: `/api/v2`
인증: `X-Emp-No` 헤더 (사번 7자리)

## GET /rooms

```json
{ "openHour": 8, "closeHour": 20, "rooms": [ { "code": "R-101", "name": "집중회의실 A" } ] }
```

## POST /reservations

요청

```json
{ "roomId": "R-101", "startAt": "2026-08-10T14:00:00", "endAt": "2026-08-10T16:00:00", "purpose": "주간회의" }
```

제약

- `endAt` 은 `startAt` 보다 뒤여야 한다
- 최소 30분, **최대 3시간**
- 같은 회의실에 겹치는 예약이 있으면 `409`

응답 `201`

```json
{ "id": 1024, "status": "CONFIRMED" }
```

## DELETE /reservations/:id

응답 `204`
