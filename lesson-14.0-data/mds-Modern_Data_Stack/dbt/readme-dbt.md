

## dbt project: jaffle_shop on DuckDB

- blog: https://rmoff.net/2022/10/20/data-engineering-in-2022-exploring-dbt-with-duckdb/
- repo: https://github.com/dbt-labs/jaffle_shop_duckdb#whats-in-this-repo

**Note:** 
- use regular Linux terminal, not VS Code terminal

### DuckDB install
https://duckdb.org/docs/installation/?environment=cli

### CLI: duckcli

```
pip install duckcli

duckcli  <path-to-duck-db-file>
```

### GUI: Dbeaver 

- install Dbeaver Universal SQL IDE
```
$ sudo snap install dbeaver-ce
$ sudo apt install path_to_deb_file
```

### Mach Speed

```
# get code
git clone https://github.com/dbt-labs/jaffle_shop_duckdb.git

# setup venv
cd jaffle_shop_duckdb
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# run build
source venv/bin/activate
dbt build
dbt docs generate
dbt docs serve --port 8099  # view documentation
# (see https://docs.getdbt.com/reference/commands/cmd-docs)

```


## DBT Tutorials

- [Oh, my dbt (data build tool)](https://towardsdatascience.com/oh-my-dbt-data-build-tool-ba43e67d2531)

- [dbt tutorial using a local PostgreSQL database](https://github.com/luchonaveiro/dbt-postgres-tutorial)
    - [My Notion Note](https://www.notion.so/GitHub-luchonaveiro-dbt-postgres-tutorial-dbt-tutorial-using-a-local-PostgreSQL-database-TODO-2df7a00da2614b4e861d025ac7e3acce)