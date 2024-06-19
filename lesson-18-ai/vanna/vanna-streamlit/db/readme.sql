-- drop table t_qa;

CREATE TABLE if not exists t_qa
(
    id_qa text NOT NULL
    , id_config text NOT NULL

    , question text
	, question_hash text

	, sql_generated text
	, sql_ts_delta float
	, sql_revised text
	, sql_hash text
	, sql_is_valid INTEGER  DEFAULT 0

	, df_data text
	
	, py_generated text
	, py_ts_delta float
	, py_revised text
	, py_hash text
	, py_is_valid INTEGER  DEFAULT 0
	, fig_generated text
	
	, summary_generated text
	, summary_ts_delta float

	, comments text
	, created_ts text
	, updated_ts text
	, is_inactive INTEGER  DEFAULT 0  
);

-- drop table t_config;
CREATE TABLE if not exists t_config
(
    id_config text NOT NULL

    , vector_db text
	, llm_vendor text
	, llm_model text
	, llm_api_key text
	, db_type text
	, db_url text

	, comments text
	, created_ts text
	, updated_ts text
	, is_inactive INTEGER  DEFAULT 0  
);

CREATE TABLE if not exists t_note
( 
    id_note text NOT NULL
    , title text NOT NULL
    , url text 
	, tags text

	, comments text
	, created_ts text
	, updated_ts text
	, is_inactive INTEGER  DEFAULT 0  
);

select * from t_config;
