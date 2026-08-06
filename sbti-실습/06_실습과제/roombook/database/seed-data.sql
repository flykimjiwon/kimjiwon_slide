-- 초기 회의실 데이터

INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-101', '집중회의실 A',  10,  4);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-102', '집중회의실 B',  10,  4);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-103', '중회의실 1',    10, 10);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-104', '중회의실 2',    11, 10);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-105', '대회의실',      11, 24);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-106', '화상회의실',    12,  8);
INSERT INTO rooms (code, name, floor, capacity) VALUES ('R-107', '교육장',        12, 40);

INSERT INTO users (emp_no, name, dept, joined_at) VALUES ('1234567', '홍길동', '디지털서비스개발부', '2019-03-04');
INSERT INTO users (emp_no, name, dept, joined_at) VALUES ('2345678', '김철수', '정보서비스개발부',   '2021-09-01');
