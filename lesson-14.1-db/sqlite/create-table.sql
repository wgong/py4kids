CREATE TABLE persons
( person_id INTEGER PRIMARY KEY AUTOINCREMENT,
  last_name VARCHAR NOT NULL,
  first_name VARCHAR,
  hire_date DATE,
  age numeric,
  note TEXT,
  score INTEGER not null default 0
);

insert into persons(last_name, first_name, hire_date, age, note)
values ('Gong', 'Anna', '2000-01-01', 22.5, 'Funny girl born on Y2K');

select * from persons;

--like ESCAPE
CREATE TABLE t(
	c TEXT
);

INSERT INTO t(c)
VALUES('10% increase'),
	('10 times decrease'),
	('100% vs. last year'),
	('20% increase next year');
	
select * from t;

SELECT c  FROM t 
WHERE c LIKE '%10\%%' ESCAPE '\';

drop table t1;