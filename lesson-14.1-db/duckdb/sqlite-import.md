## TODO: 
- [2024-06-16]
    - revise/refactor WatchETF/stooq/gwg_db.py for duckdb

## DONE: 
- [2024-06-15]
    - Done migrating table, 
    - Done creating index


https://duckdb.org/docs/guides/database_integration/sqlite

## Install duckdb on Linux

download binary from https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip

```
cd ~/Downloads
unzip duckdb_cli-linux-amd64.zip
mv duckdb ~/.local/bin
```
## install sqlite extension

```
INSTALL sqlite;  # once
```

## attach
```
duckdb stooq.duckdb  # will save sqlite as duckdb
LOAD sqlite;
ATTACH 'db_gwg.sqlite' AS src (TYPE sqlite);
USE src;
SHOW TABLES;

.databases

use stooq;

create table quote_ta as select * from src.quote_ta;
create table quote_ta_hist as select * from src.quote_ta_hist;


create table ta_stat as select * from src.ta_stat;
create table ticker as select * from src.ticker;
create table list as select * from src.list;
create table list_ticker as select * from src.list_ticker;
create table list_watch as select * from src.list_watch;
create table notes as select * from src.notes;
create table process_status as select * from src.process_status;
create table quote_daily as select * from src.quote_daily;
create table list_research as select * from src.list_research;
create table list_ticker_etf as select * from src.list_ticker_etf;
create table list_ticker_etf_update as select * from src.list_ticker_etf_update;
create table ticker_etf as select * from src.ticker_etf;
create table ticker_extra as select * from src.ticker_extra;
create table ticker_stooq as select * from src.ticker_stooq;
.exit
```

Issues:
```
D create table quote_ta as select * from src.quote_ta;
Mismatch Type Error: Invalid type in column "Volume": column was declared as integer, found "318210.51099158" of type "float" instead.
D create table quote_ta_hist as select * from src.quote_ta_hist;
Mismatch Type Error: Invalid type in column "Volume": column was declared as integer, found "1086344.3319749" of type "float" instead.

```

Fix:
```
alter table quote_ta add column Volume_2 real;
update quote_ta set Volume_2 = CAST(Volume AS REAL);
alter table quote_ta drop column Volume;
alter table quote_ta rename column Volume_2 to Volume;

alter table quote_ta_hist add column Volume_2 real;
update quote_ta_hist set Volume_2 = CAST(Volume AS REAL);
alter table quote_ta_hist drop column Volume;
alter table quote_ta_hist rename column Volume_2 to Volume;

```

/home/gongai/snap/dbeaver-ce/304/.local/share/DBeaverData/workspace6/General/Scripts/gwg_db_stooq.sql



CREATE UNIQUE INDEX list_idx on list (list) ;
CREATE INDEX list_idx2 on list(note);
CREATE INDEX list_research_idx on list_research(list,ticker);
CREATE INDEX list_ticker_idx on list_ticker(list,ticker);
CREATE INDEX list_watch_idx on list_watch(list,ticker);
CREATE INDEX quote_daily_idx on quote_daily(ticker, date_);
CREATE INDEX quote_ta_hist_idx on quote_ta_hist (ticker, date_) ;
CREATE INDEX quote_ta_hist_idx1 on quote_ta_hist(ticker);
CREATE INDEX quote_ta_hist_idx2 on quote_ta_hist(date_);
CREATE INDEX ta_stat_idx on ta_stat (date_, ticker) ;
CREATE UNIQUE INDEX ticker_idx on ticker (ticker) ;
CREATE UNIQUE INDEX ticker_stooq_idx on ticker_stooq (ticker);
