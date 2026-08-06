#!/usr/bin/env python3
"""보관 기간이 지난 예약을 정리한다."""

RETENTION_DAYS = 30
TARGET_TABLE = "reservations"


def find_expired(conn, retention_days=RETENTION_DAYS):
    sql = (
        f"SELECT id FROM {TARGET_TABLE} "
        "WHERE status = 'CANCELLED' AND end_at < NOW() - INTERVAL '%s days'"
    )
    return conn.execute(sql, (retention_days,)).fetchall()


def archive(conn, ids):
    if not ids:
        print("정리 대상 없음")
        return 0
    conn.execute("INSERT INTO audit_log (action, target_id) VALUES ('ARCHIVE', %s)", ids)
    return len(ids)


if __name__ == "__main__":
    print(f"보관 기간 {RETENTION_DAYS}일 기준으로 정리합니다")
