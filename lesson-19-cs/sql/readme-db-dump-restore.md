backup data from postgresql v15
```
pg_dumpall -U postgres -h localhost -p 5432 > backup_all_databases.sql
```

restore data 
```
psql -U postgres -h localhost -p 5433 -f backup_all_databases.sql
```

https://neon.com/guides/vector-search
https://neon.com/blog/optimizing-vector-search-performance-with-pgvector

CREATE EXTENSION vector;

SQL state: 0A000
Detail: Could not open extension control file "C:/Program Files/PostgreSQL/17/share/extension/vector.control": No such file or directory.
Hint: The extension must first be installed on the system where PostgreSQL is running

Install on Windows requires c++ compiler and VS Studio

https://neon.com/guides/neon-mcp-server