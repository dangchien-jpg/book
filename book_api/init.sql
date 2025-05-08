CREATE DATABASE local_db;
USE local_db;
CREATE TABLE books (
  id int(10) NOT NULL,
  title varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (id)
);
INSERT INTO books VALUES(1, 'Book 1');
INSERT INTO books VALUES(2, 'Book 2');


