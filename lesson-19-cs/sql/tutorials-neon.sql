--COALESCE
SELECT COALESCE (NULL, 3, 1, 2);

CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  product VARCHAR (100) NOT NULL,
  price NUMERIC NOT NULL,
  discount NUMERIC
);

INSERT INTO items (product, price, discount)
VALUES
  ('A', 1000, 10),
  ('B', 1500, 20),
  ('C', 800, 5),
  ('D', 500, NULL)
returning *;

SELECT
  product,
  (
    price - COALESCE(discount, 0)
  ) AS net_price,
  round(COALESCE(discount, 0) / price * 100, 2) as pct_discount
FROM
  items;


--case
SELECT
  title,
  length,
  CASE 
  	WHEN length > 0 AND length <= 50 THEN 'Short' 
	WHEN length > 50 AND length <= 120 THEN 'Medium' 
	WHEN length > 120 THEN 'Long' 
  END duration
FROM
  film
ORDER BY
  duration, length, title;

SELECT
  SUM (
    CASE WHEN rental_rate = 0.99 THEN 1 ELSE 0 END
  ) AS "Economy",
  SUM (
    CASE WHEN rental_rate = 2.99 THEN 1 ELSE 0 END
  ) AS "Mass",
  SUM (
    CASE WHEN rental_rate = 4.99 THEN 1 ELSE 0 END
  ) AS "Premium"
FROM
  film;

-- #####################################
-- vector 

-- CREATE EXTENSION vector;
-- needs compiler installed

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

SELECT uuid_generate_v4();
-- b33608ca-5f54-4d17-b0e5-6bc79fa40b83

-- #####################################
-- uuid 
CREATE TABLE contacts (
    contact_id uuid DEFAULT gen_random_uuid(),
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    phone VARCHAR,
    PRIMARY KEY (contact_id)
);

select * from contacts;

INSERT INTO contacts ( first_name, last_name, email, phone)
VALUES
  ('John', 'Smith', 'john.smith@example.com',  '408-237-2345'),
  ('Jane', 'Smith', 'jane.smith@example.com', '408-237-2344'),
  ('Alex', 'Smith', 'alex.smith@example.com', '408-237-2343')
RETURNING *;


-- #####################################
-- array
CREATE TABLE contacts_arr (
  id SERIAL PRIMARY KEY,
  name VARCHAR (100),
  phones TEXT []
);

INSERT INTO contacts_arr (name, phones)
VALUES('John Doe', ARRAY [ '(408)-589-5846','(408)-589-5555' ]);

INSERT INTO contacts_arr (name, phones)
VALUES('Lily Bush','{"(408)-589-5841"}'),
      ('William Gate','{"(408)-589-5842","(408)-589-58423"}');

select * from contacts_arr;
select name, phones[1] from contacts_arr;

SELECT
  name
FROM
  contacts_arr
WHERE
  phones [ 2 ] = '(408)-589-58423';
  
-- #####################################
-- upsert
CREATE TABLE inventory(
   id INT PRIMARY KEY,
   name VARCHAR(255) NOT NULL,
   price DECIMAL(10,2) NOT NULL,
   quantity INT NOT NULL
);

INSERT INTO inventory(id, name, price, quantity)
VALUES
	(1, 'A', 15.99, 100),
	(2, 'B', 25.49, 50),
	(3, 'C', 19.95, 75)
RETURNING *;


-- The DO UPDATE changes the price and quantity of the product to the new values being inserted. 
-- The EXCLUDED allows you to access the new values.
INSERT INTO inventory (id, name, price, quantity)
VALUES (1, 'A', 16.99, 120)
ON CONFLICT(id)
DO UPDATE 
SET
  price = EXCLUDED.price,
  quantity = EXCLUDED.quantity;
  
select * from inventory where id=1;

INSERT INTO inventory (id, name, price, quantity)
VALUES (1, 'A', 17.99, 200), 
	(10, 'E', 50, 5),
	(11, 'F', 9.95, 175)
ON CONFLICT(id)
DO NOTHING;

select * from inventory;


-- #####################################
-- merge : useful for updating target tables with incremental updates
-- https://neon.com/postgresql/postgresql-tutorial/postgresql-merge

-- products, inventory example

-- Create the main products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    price DECIMAL(10,2),
    stock INTEGER,
    status TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some initial data
INSERT INTO products (name, price, stock, status) 
VALUES
    ('Laptop', 999.99, 50, 'active'),
    ('Keyboard', 79.99, 100, 'active'),
    ('Mouse', 29.99, 200, 'active')
RETURNING *;

-- Create a table for our updates
CREATE TABLE product_updates (
    name TEXT,
    price DECIMAL(10,2),
    stock INTEGER,
    status TEXT
);

-- Insert mixed update data (new products, updates, and discontinuations)
INSERT INTO product_updates 
VALUES
    ('Laptop', 1099.99, 75, 'active'),      -- Update: price and stock change
    ('Monitor', 299.99, 30, 'active'),      -- Insert: new product
    ('Keyboard', NULL, 0, 'discontinued'),  -- Delete: mark as discontinued
    ('Headphones', 89.99, 50, 'active');    -- Insert: another new product
	
select * from product_updates;
select * from products;

-- Now let's see how PostgreSQL 17's enhanced MERGE command can handle all three operations (INSERT, UPDATE, DELETE) while providing detailed feedback through the RETURNING clause:
-- Insert mixed update data (new products, updates, and discontinuations)
MERGE INTO products p
USING product_updates u
ON p.name = u.name
WHEN MATCHED AND u.status = 'discontinued' THEN
    DELETE
WHEN MATCHED AND u.status = 'active' THEN
    UPDATE SET
        price = COALESCE(u.price, p.price),
        stock = u.stock,
        status = u.status,
        last_updated = CURRENT_TIMESTAMP
WHEN NOT MATCHED AND u.status = 'active' THEN
    INSERT (name, price, stock, status)
    VALUES (u.name, u.price, u.stock, u.status)
RETURNING
    merge_action() as action,
    p.product_id,
    p.name,
    p.price,
    p.stock,
    p.status,
    p.last_updated;

/*

"UPDATE"	1	"Laptop"	1099.99	75	"active"	"2025-09-07 15:54:00.446455"
"INSERT"	4	"Monitor"	299.99	30	"active"	"2025-09-07 15:54:00.446455"
"DELETE"	2	"Keyboard"	79.99	100	"active"	"2025-09-07 15:50:42.954222"
"INSERT"	5	"Headphones"	89.99	50	"active"	"2025-09-07 15:54:00.446455"
*/

select * from products;
select * from product_updates;




-- date
SHOW TIMEZONE;
SELECT LOCALTIME;
SELECT timezone('America/Los_Angeles','2016-06-01 00:00');
SELECT timezone('America/Los_Angeles',now());

select now(), 
	now()::date, 
	current_timestamp, -- same as now()
	current_date, CURRENT_TIME, 
	TIMEOFDAY();

SELECT TO_CHAR(CURRENT_DATE, 'dd/mm/yyyy') as dt1, 
	TO_CHAR(CURRENT_DATE, 'yyyy-mm-dd') as dt2;

SELECT TO_CHAR(CURRENT_DATE, 'Mon dd, yyyy');

SELECT
	now(),
	now() - INTERVAL '2 year 3 hours 20 minutes'
             AS "3 hours 20 minutes ago of last year";

SELECT INTERVAL '2h 50m' + INTERVAL '10m'; -- 03:00:00
SELECT INTERVAL '2h 50m' - INTERVAL '50m'; -- 02:00:00
SELECT 600 * INTERVAL '1 minute'; -- 10:00:00



-- recursive query 
CREATE TABLE employees (
  employee_id SERIAL PRIMARY KEY,
  full_name VARCHAR NOT NULL,
  manager_id INT
);
INSERT INTO employees (employee_id, full_name, manager_id)
VALUES
  (1, 'Michael North', NULL),
  (2, 'Megan Berry', 1),
  (3, 'Sarah Berry', 1),
  (4, 'Zoe Black', 1),
  (5, 'Tim James', 1),
  (6, 'Bella Tucker', 2),
  (7, 'Ryan Metcalfe', 2),
  (8, 'Max Mills', 2),
  (9, 'Benjamin Glover', 2),
  (10, 'Carolyn Henderson', 3),
  (11, 'Nicola Kelly', 3),
  (12, 'Alexandra Climo', 3),
  (13, 'Dominic King', 3),
  (14, 'Leonard Gray', 4),
  (15, 'Eric Rampling', 4),
  (16, 'Piers Paige', 7),
  (17, 'Ryan Henderson', 7),
  (18, 'Frank Tucker', 8),
  (19, 'Nathan Ferguson', 8),
  (20, 'Kevin Rampling', 8)
returning *;

--recursive CTE to find all subordinates of the manager with the id 2.
WITH RECURSIVE subordinates AS (
  -- anchor member
  SELECT
    employee_id,
    manager_id,
    full_name
  FROM
    employees
  WHERE
    employee_id = 7 --2
--    employee_id = 6 -- no subordinates
  UNION
  -- recursive term
  SELECT
    e.employee_id,
    e.manager_id,
    e.full_name
  FROM
    employees e
    INNER JOIN subordinates s ON s.employee_id = e.manager_id
)
SELECT * FROM subordinates;





