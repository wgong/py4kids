-- https://www.sqlite.org/lang_with.html#:~:text=The%20recursive%2Dselect%20is%20allowed,2020%2D12%2D01
WITH RECURSIVE
cnt(x) AS (
	 SELECT 1
	 UNION ALL
	 SELECT x+1 FROM cnt
		LIMIT 100  -- better than where x < 100
)
SELECT x FROM cnt;

-- org chart
WITH RECURSIVE
  sub_org(employeeid, reportsto, firstname, lastname, level) AS (
    SELECT org.employeeid, org.reportsto, org.firstname, org.lastname, 0 
	FROM employees org
		where org.reportsto is null
    UNION all
    SELECT org.employeeid, org.reportsto, org.firstname, org.lastname, sub_org.level+1
	FROM employees org join sub_org
		on org.reportsto = sub_org.employeeid
	--ORDER BY 5  -- breadth-first search
	ORDER BY 5 desc  -- depth-first search
  )
SELECT substr('..........',1,level*3) || FirstName as First_Name FROM sub_org
--select EmployeeId,ReportsTo,FirstName,level from sub_org
--SELECT * FROM sub_org
;




-- https://docs.oracle.com/cd/E17952_01/mysql-8.0-en/with.html#common-table-expressions-recursive-fibonacci-series
WITH RECURSIVE 
fibonacci (n, fib_n, next_fib_n) AS
(
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib_n, fib_n + next_fib_n
    FROM fibonacci 
	limit 1000
)
SELECT * FROM fibonacci
	where n=67;