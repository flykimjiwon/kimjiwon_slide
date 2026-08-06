-- 001 : 회의실 테이블 생성
-- 적용일 2026-06-14

BEGIN;

CREATE TABLE IF NOT EXISTS rooms (
  id       SERIAL PRIMARY KEY,
  code     VARCHAR(10) NOT NULL UNIQUE,
  name     VARCHAR(60) NOT NULL,
  floor    SMALLINT    NOT NULL,
  capacity SMALLINT    NOT NULL,
  active   BOOLEAN     NOT NULL DEFAULT TRUE
);

COMMIT;
