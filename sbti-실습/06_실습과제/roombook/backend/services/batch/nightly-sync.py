#!/usr/bin/env python3
"""야간 동기화 배치 — 인사 시스템에서 사번/부서를 받아 users 테이블을 갱신한다."""

import datetime

BATCH_NAME = "nightly-sync"
SOURCE_SYSTEM = "HR-MASTER"
CHUNK_SIZE = 500


def fetch_employees(cursor_date):
    """인사 시스템에서 변경분을 가져온다 (실습용 더미)."""
    return [
        {"emp_no": "1234567", "name": "홍길동", "dept": "디지털서비스개발부"},
        {"emp_no": "2345678", "name": "김철수", "dept": "정보서비스개발부"},
    ]


def upsert_users(rows):
    for row in rows:
        print(f"upsert {row['emp_no']} {row['dept']}")
    return len(rows)


# TODO: 실패한 청크만 재시도하는 로직 추가
def main():
    started = datetime.datetime.now()
    rows = fetch_employees(started.date())
    count = upsert_users(rows)
    print(f"[{BATCH_NAME}] {count}건 처리 · 소스={SOURCE_SYSTEM}")


if __name__ == "__main__":
    main()
