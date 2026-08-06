-- roombook 스키마 (실습용)

CREATE TABLE rooms (
  id        SERIAL PRIMARY KEY,
  code      VARCHAR(10) NOT NULL UNIQUE,
  name      VARCHAR(60) NOT NULL,
  floor     SMALLINT    NOT NULL,
  capacity  SMALLINT    NOT NULL,
  active    BOOLEAN     NOT NULL DEFAULT TRUE
);
CREATE INDEX idx_rooms_floor ON rooms (floor);

CREATE TABLE users (
  emp_no    VARCHAR(7) PRIMARY KEY,
  name      VARCHAR(30) NOT NULL,
  dept      VARCHAR(60) NOT NULL,
  joined_at DATE
);
CREATE INDEX idx_users_dept ON users (dept);

CREATE TABLE reservations (
  id        SERIAL PRIMARY KEY,
  room_id   VARCHAR(10) NOT NULL,
  emp_no    VARCHAR(7)  NOT NULL,
  start_at  TIMESTAMP   NOT NULL,
  end_at    TIMESTAMP   NOT NULL,
  purpose   VARCHAR(60),
  status    VARCHAR(12) NOT NULL DEFAULT 'CONFIRMED'
);
-- 인덱스는 002-add-index.sql 에서 추가한다

CREATE TABLE audit_log (
  id         SERIAL PRIMARY KEY,
  action     VARCHAR(20) NOT NULL,
  target_id  INTEGER,
  actor      VARCHAR(7),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
