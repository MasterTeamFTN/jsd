-- Time: 2021-04-08 09:08:51.300368
-- Database: mysql

CREATE TABLE Test (
    id number PRIMARY KEY,
    name varchar NOT NULL,
    subject_id_tests varchar FOREIGN KEY REFERENCES Subject(id),
);

CREATE TABLE Subject (
    id varchar PRIMARY KEY,
    name varchar NOT NULL,
);
