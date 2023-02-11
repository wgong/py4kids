-- Databricks notebook source
show databases

-- COMMAND ----------

create database test_db

-- COMMAND ----------

show databases

-- COMMAND ----------

use test_db

-- COMMAND ----------

show tables

-- COMMAND ----------

use default

-- COMMAND ----------

show tables

-- COMMAND ----------

use test_db;
select * from default.flights_parq

-- COMMAND ----------

SELECT current_database()

-- COMMAND ----------

create table flights_parquet as select * from default.flights_parq

-- COMMAND ----------

select count(*) from flights_parquet

-- COMMAND ----------

select * from flights_parquet where upper(DEST_COUNTRY_NAME) in ('UNITED STATES','EGYPT')

-- COMMAND ----------

SELECT
  DEST_COUNTRY_NAME,
  CASE WHEN upper(DEST_COUNTRY_NAME) = 'UNITED STATES' THEN 1
       WHEN upper(DEST_COUNTRY_NAME) = 'EGYPT' THEN 0
       ELSE -1 END as US_FLAG
FROM flights_parquet

-- COMMAND ----------

CREATE VIEW IF NOT EXISTS flights_nest AS
  SELECT (DEST_COUNTRY_NAME, ORIGIN_COUNTRY_NAME) as country, count FROM flights_parquet

-- COMMAND ----------

show tables

-- COMMAND ----------

select * from flights_nest

-- COMMAND ----------

SELECT country.*, count FROM flights_nest

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW flights_agg AS
  SELECT DEST_COUNTRY_NAME, collect_list(count) as collected_counts
  FROM default.flights_parq GROUP BY DEST_COUNTRY_NAME

-- COMMAND ----------

select * from flights_agg

-- COMMAND ----------

SELECT DEST_COUNTRY_NAME, explode(collected_counts)  FROM flights_agg where upper(DEST_COUNTRY_NAME) = 'UNITED STATES'

-- COMMAND ----------

show functions

-- COMMAND ----------

SHOW SYSTEM FUNCTIONS

-- COMMAND ----------

SHOW user FUNCTIONS

-- COMMAND ----------

SHOW FUNCTIONS "u*";

-- COMMAND ----------

SHOW FUNCTIONS LIKE "collect*";

-- COMMAND ----------

set spark.sql.shuffle.partitions=20

-- COMMAND ----------

set

-- COMMAND ----------


