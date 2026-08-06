#!/bin/sh
# roombook 헬스체크 — 배포 후 상태 확인용

HOST="${1:-http://localhost:8080}"
RETRY=10
SLEEP=3

echo "health check -> $HOST/healthz"

i=1
while [ "$i" -le "$RETRY" ]; do
  if curl -fsS "$HOST/healthz" > /dev/null 2>&1; then
    echo "ok ($i번째 시도)"
    exit 0
  fi
  echo "  대기중... ($i/$RETRY)"
  i=$((i + 1))
  sleep "$SLEEP"
done

echo "실패: $RETRY번 시도해도 응답 없음"
exit 1
