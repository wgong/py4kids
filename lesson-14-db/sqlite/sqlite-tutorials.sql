select count(*) from albums;

select * from albums limit 5;

select ArtistId, count(*) from albums group by ArtistId;

SELECT
	trackid,
	name,
	composer,
	unitprice
FROM
	tracks;
	
-- order by
SELECT
	name,
	milliseconds, 
	albumid
FROM
	tracks
ORDER BY
	albumid ASC,
    milliseconds DESC;
	
SELECT 
    TrackId, 
    Name, 
    Composer 
FROM 
    tracks
ORDER BY 
    Composer -- NULLS LAST
	;
	
SELECT DISTINCT city
FROM customers
ORDER BY city;

--for large dataset, use group by to dedup (not distinct)
select City
from customers
group by city;

select count(*) from 
(
	SELECT DISTINCT city
	FROM customers
);
--53

select count(*) from 
(
	select City
	from customers
	group by city
);
--53

SELECT
   name,
   milliseconds,
   bytes,
   albumid
FROM
   tracks
WHERE
   albumid <= 5 AND milliseconds > 250000;

SELECT
	trackId,
	name
FROM
	tracks
LIMIT 10 OFFSET 10;

SELECT
	trackid,
	name,
	bytes
FROM
	tracks
ORDER BY
	bytes DESC
LIMIT 10;

SELECT
    InvoiceId,
    BillingAddress,
    Total
FROM
    invoices
WHERE
    Total BETWEEN 14.91 and 18.86    
ORDER BY
    Total; 
	
SELECT
    InvoiceId,
    BillingAddress,
    InvoiceDate,
    Total
FROM
    invoices
WHERE
    InvoiceDate BETWEEN '2010-01-01' AND '2010-01-31'
ORDER BY
    InvoiceDate; 
	
SELECT
	TrackId,
	Name,
	Mediatypeid
FROM
	Tracks
WHERE
	MediaTypeId IN (1, 2)
ORDER BY
	Name ASC;
	
SELECT
	TrackId, 
	Name, 
	AlbumId
FROM
	Tracks
WHERE
	AlbumId IN (
		SELECT
			AlbumId
		FROM
			Albums
		WHERE
			ArtistId = 12
	);
	
SELECT
	trackid,
	name	
FROM
	tracks
WHERE
	name LIKE '%Wild%';
	
SELECT
	trackid,
	name
FROM
	tracks
WHERE
	name GLOB 'Man*' or name GLOB '?ere*' or name GLOB '*[1-9]*';	

SELECT
	trackid,
	name
FROM
	tracks
WHERE
	name GLOB '*[^1-9]*';
	
SELECT
    Name, 
    Composer
FROM
    tracks
WHERE
    Composer IS NULL
ORDER BY 
    Name;   

SELECT
    Name, 
    Composer
FROM
    tracks
WHERE
    Composer IS NOT NULL
ORDER BY 
    Name;       

-- joins
-- inner
SELECT 
    b.*, a.*
FROM 
    albums b
INNER JOIN artists a
    ON a.ArtistId = b.ArtistId;

SELECT
    trackid,
    tracks.name AS track,
    albums.title AS album,
    artists.name AS artist
FROM
    tracks
    INNER JOIN albums ON albums.albumid = tracks.albumid
    INNER JOIN artists ON artists.artistid = albums.artistid;

--LEFT	
-- list albums with associated artist (if any)
SELECT 
    b.*, a.*
FROM 
    albums b 
LEFT JOIN artists a 
    ON a.ArtistId = b.ArtistId;
	
-- list artists  with associated albums (if any)
SELECT 
    b.*, a.*
FROM 
    artists a 
LEFT JOIN albums b
    ON a.ArtistId = b.ArtistId;	

SELECT
    Name,
    Title
FROM
    artists
LEFT JOIN albums ON
    artists.ArtistId = albums.ArtistId
WHERE Title IS NULL   
ORDER BY Name;

-- CROSS
CREATE TABLE t_products(
    product text NOT null
);

INSERT INTO t_products(product)
VALUES('P1'),('P2'),('P3');



CREATE TABLE t_calendars(
    y int NOT NULL,
    m int NOT NULL
);

INSERT INTO t_calendars(y,m)
VALUES 
    (2019,1),
    (2019,2),
    (2019,3);

SELECT * 
FROM t_products
CROSS JOIN t_calendars;

-- self-join for parent/child relationship
SELECT m.firstname || ' ' || m.lastname AS 'Manager',
       e.firstname || ' ' || e.lastname AS 'Direct report' 
FROM employees e
INNER JOIN employees m ON m.employeeid = e.reportsto
ORDER BY manager;

SELECT m.firstname || ' ' || m.lastname AS 'Manager',
       e.firstname || ' ' || e.lastname AS 'Direct report' 
FROM employees e
LEFT JOIN employees m ON m.employeeid = e.reportsto
ORDER BY manager;

-- find the employees located in the same city
SELECT DISTINCT
	e1.city,
	e1.firstName || ' ' || e1.lastname AS fullname
FROM
	employees e1
INNER JOIN employees e2 ON e2.city = e1.city 
   AND (e1.firstname <> e2.firstname AND e1.lastname <> e2.lastname)
ORDER BY
	e1.city;

--group by
SELECT
	albumid,
	COUNT(trackid)
FROM
	tracks
GROUP BY
	albumid
order by count(trackid) desc;

SELECT
	tracks.albumid,
	title,
	COUNT(trackid)
FROM
	tracks
INNER JOIN albums ON albums.albumid = tracks.albumid
GROUP BY
	tracks.albumid
	HAVING COUNT(trackid) > 15;

SELECT
	albumid,
	SUM(milliseconds)/60000 length_mins,
	SUM(bytes) size
FROM
	tracks
GROUP BY
	albumid;

SELECT
	tracks.albumid,
	title,
	min(milliseconds),
	max(milliseconds),
	round(avg(milliseconds),2)
FROM
	tracks
INNER JOIN albums ON albums.albumid = tracks.albumid
GROUP BY
	tracks.albumid;
	
SELECT
   STRFTIME('%Y', InvoiceDate) InvoiceYear, 
   COUNT(InvoiceId) InvoiceCount
FROM
   invoices
GROUP BY
   STRFTIME('%Y', InvoiceDate)
ORDER BY
   InvoiceYear;

SELECT
   albumid,
   COUNT(trackid)
FROM
   tracks
GROUP BY
   albumid
HAVING 
   albumid between 100 and 200
   and COUNT(albumid) BETWEEN 18 AND 20
ORDER BY albumid;

SELECT
	tracks.AlbumId,
	title,
	SUM(Milliseconds) AS length
FROM
	tracks
INNER JOIN albums ON albums.AlbumId = tracks.AlbumId
GROUP BY
	tracks.AlbumId 
HAVING
	length > 60000000;
--UNION
CREATE TABLE t1(
    v1 INT
);
 
INSERT INTO t1(v1)
VALUES(1),(2),(3);
 
CREATE TABLE t2(
    v2 INT
);
INSERT INTO t2(v2)
VALUES(2),(3),(4);

-- union removes duplicate rows but union all keep all ROWS
SELECT v1
  FROM t1
UNION
SELECT v2
  FROM t2;
  
SELECT v1
  FROM t1
UNION ALL
SELECT v2
  FROM t2;
  
SELECT v1
FROM t1
INTERSECT 
SELECT v2
FROM t2;

SELECT v1
FROM t1
EXCEPT 
SELECT v2
FROM t2;

SELECT v2
FROM t2
EXCEPT
SELECT v1
FROM t1;

select * from (
	SELECT v1
	  FROM t1
	UNION
	SELECT v2
	  FROM t2)
EXCEPT
select * from (
	SELECT v1
	FROM t1
	INTERSECT 
	SELECT v2
	FROM t2
);


SELECT FirstName, LastName, 'Employee' AS Type
FROM employees
UNION
SELECT FirstName, LastName, 'Customer'
FROM customers
ORDER BY FirstName, LastName;
  
SELECT customerid,
       firstname,
       lastname
  FROM customers
 WHERE supportrepid IN (
           SELECT employeeid
             FROM employees
            WHERE country = 'Canada'
       );

SELECT
	AVG(album.size)
FROM
	(
		SELECT
			SUM(bytes) SIZE
		FROM
			tracks
		GROUP BY
			albumid
	) AS album;

SELECT albumid,
       title
  FROM albums
 WHERE 10000000 > (
                      SELECT sum(bytes) 
                        FROM tracks
                       WHERE tracks.AlbumId = albums.AlbumId
                  )
 ORDER BY title;
 
SELECT albumid,
       title,
       (
           SELECT count(trackid) 
             FROM tracks
            WHERE tracks.AlbumId = albums.AlbumId
       )
       tracks_count
  FROM albums
 ORDER BY tracks_count DESC;
 -- same as 
 SELECT a.albumid,
       a.title,
	   count(t.trackid) as tracks_count
  FROM albums a INNER join tracks t on t.AlbumId = a.AlbumId
  group by a.AlbumId, a.Title
 ORDER BY tracks_count DESC;
 
SELECT
    CustomerId,
    FirstName,
    LastName,
    Company
FROM
    Customers c
WHERE
    EXISTS (
        SELECT 
            1 
        FROM 
            Invoices
        WHERE 
            CustomerId = c.CustomerId
    )
ORDER BY
    FirstName,
    LastName; 

SELECT
   CustomerId, 
   FirstName, 
   LastName, 
   Company
FROM
   Customers c
WHERE
   CustomerId IN (
      SELECT
         CustomerId
      FROM
         Invoices
   )
ORDER BY
   FirstName, 
   LastName;

-- CASE

-- simple case
SELECT customerid,
       firstname,
       lastname,
       CASE country 
           WHEN 'USA' 
               THEN 'Domestic' 
           ELSE 'Foreign' 
       END CustomerGroup
FROM 
    customers
ORDER BY 
    LastName,
    FirstName;  
	
-- searched CASE
SELECT
	trackid,
	name,
	CASE
		WHEN milliseconds < 60000 THEN
			'short'
		WHEN milliseconds > 60000 AND milliseconds < 300000 THEN 'medium'
		ELSE
			'long'
		END category
FROM
	tracks;
	
--WITH
with cust as (SELECT customerid,
       firstname,
       lastname,
       CASE country 
           WHEN 'USA' 
               THEN 'Domestic' 
           ELSE 'Foreign' 
       END CustomerGroup
FROM 
    customers
ORDER BY 
    LastName,
    FirstName
) 
select CustomerGroup, count(*) 
 from cust group by CustomerGroup;
 
-- don't use UNION because it will incur memory cost
-- https://www.sqlite.org/lang_with.html
WITH RECURSIVE
  cnt(x) AS (
  VALUES(1) 
  UNION ALL 
  SELECT x+1 FROM cnt 
  WHERE x<100000
)
SELECT x FROM cnt;
--16ms

-- optimized
WITH RECURSIVE
  cnt(x) AS (
     SELECT 1
     UNION ALL
     SELECT x+1 FROM cnt
      LIMIT 100000
)
SELECT x FROM cnt;
--24ms
 
-- dynamic typing
SELECT
	typeof(100),
	typeof(10.0),
	typeof('100'),
	typeof(x'1000'),
	typeof(NULL);	

CREATE TABLE test_datatypes (
	id INTEGER PRIMARY KEY,
	val
);

INSERT INTO test_datatypes (val)
VALUES
	(1),
	(2),
	(10.1),
	(20.5),
	('A'),
	('B'),
	(NULL),
	(x'0010'),
	(x'0011');
	
INSERT INTO test_datatypes (val)
VALUES
	(1.01),
	('A-1');
	
SELECT
	id,
	val,
	typeof(val)
FROM
	test_datatypes;	
	
SELECT
	id,
	val,
	typeof(val)
FROM
	test_datatypes
order by val NULLS LAST;




-- datetime functions
--https://www.sqlitetutorial.net/sqlite-date-functions/
--https://www.sqlitetutorial.net/sqlite-date-functions/sqlite-strftime-function/

-- stored as ISO8601 string : YYYY-MM-DD HH:MM:SS.SSS 
CREATE TABLE t_datetime(
   d1 text, 
   d2 text
);	

SELECT datetime('now','localtime');
--2022-01-15 09:03:43
SELECT datetime('now');
--2022-01-15 14:01:53   
INSERT INTO t_datetime (d1, d2)
VALUES(datetime('now'),datetime('now', 'localtime'));

SELECT
	d1,
	typeof(d1),
	d2,
	typeof(d2)
FROM
	t_datetime;
	
--stored as REAL
--Julian day numbers, since noon in Greenwich on November 24, 4714 B.C. 
--based on the proleptic Gregorian calendar
CREATE TABLE t_datetime_real(
   d1 real
);
INSERT INTO t_datetime_real (d1)
VALUES(julianday('now'));
SELECT
	d1,
	typeof(d1)
FROM
	t_datetime_real;
	
SELECT
	date(d1),
	time(d1),
	datetime(d1,"localtime")
FROM
	t_datetime_real;
	
--stored as INTEGER
-- UNIX time seconds since 1970-01-01 00:00:00 UTC
CREATE TABLE t_datetime_int (d1 int);
INSERT INTO t_datetime_int (d1)
VALUES(strftime('%s','now'));

SELECT d1, datetime(d1,'unixepoch')
FROM t_datetime_int;


INSERT INTO artists (name)
VALUES ('Hillary Hahn'), ('Li Guyi');

create table artists_backup as select * from artists;

UPDATE employees
SET email = LOWER(firstname || "." || lastname || "@chinookcorp.com")
where EmployeeId = 1;

select * from artists_backup where name LIKE '%Santana%';
DELETE FROM artists_backup WHERE name LIKE '%Santana%';

-- no truncate table, just use delete without where-clause
 DELETE FROM artists_backup;
 select * from artists_backup;
 drop table artists_backup;
 
--replace = delete + insert
CREATE TABLE IF NOT EXISTS positions (
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	min_salary NUMERIC
);

INSERT INTO positions (title, min_salary)
VALUES ('DBA', 120000),
       ('Developer', 100000),
       ('Architect', 150000);
	   
SELECT * FROM positions;

CREATE UNIQUE INDEX idx_positions_title 
ON positions (title);

REPLACE INTO positions (title, min_salary)
VALUES('Full Stack Developer', 140000);

REPLACE INTO positions (title, min_salary)
VALUES('Architect', 160000);

--full-text search
-- https://www.sqlitetutorial.net/sqlite-full-text-search/
CREATE VIRTUAL TABLE posts 
USING FTS5(title, body);

INSERT INTO posts(title,body)
VALUES('Learn SQlite FTS5','This tutorial teaches you how to perform full-text search in SQLite using FTS5'),
('Advanced SQlite Full-text Search','Show you some advanced techniques in SQLite full-text searching'),
('SQLite Tutorial','Help you learn SQLite quickly and effectively');

SELECT * FROM posts;

SELECT * 
FROM posts 
WHERE posts MATCH 'fts5';

SELECT * 
FROM posts 
WHERE posts = 'fts5';

SELECT * 
FROM posts('fts5');

SELECT * 
FROM posts 
WHERE posts MATCH 'text' 
ORDER BY rank;

SELECT * 
FROM posts 
WHERE posts MATCH 'learn SQLite';

SELECT * 
FROM posts 
WHERE posts MATCH 'advanced';

SELECT * 
FROM posts
WHERE posts = 'search*';


SELECT * 
FROM posts 
WHERE posts MATCH 'search AND (sqlite OR help) NOT tutorial';


SELECT highlight(posts,0, '<b>', '</b>') title, 
       highlight(posts,1, '<b>', '</b>') body
FROM posts 
WHERE posts MATCH 'SQLite'
ORDER BY rank;
