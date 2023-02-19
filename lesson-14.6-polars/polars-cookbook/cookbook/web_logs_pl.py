import polars as pl
def set_types(dataf):
    return (dataf
            .with_columns([
                 pl.col("timestamp").str.strptime(pl.Datetime, fmt="%m/%d/%y %H:%M:%S"),
                 pl.col("guild") != -1,
             ]))

def sessionize(dataf, threshold=1_000_000):
    return (dataf
             .sort(["char", "timestamp"])
             .with_columns([
                 (pl.col("timestamp").diff().cast(pl.Int64) > threshold).fill_null(True).alias("ts_diff"),
                 (pl.col("char").diff() != 0).fill_null(True).alias("char_diff"),
             ])
             .with_columns([
                 (pl.col("ts_diff") | pl.col("char_diff")).alias("new_session_mark")
             ])
             .with_columns([
                 pl.col("new_session_mark").cumsum().alias("session")
             ])
             .drop(['char_diff', 'ts_diff', 'new_session_mark']))

def add_features(dataf):
    return (dataf
             .with_columns([
                 pl.lit(1).alias("one")
             ])
             .with_columns([
                 pl.col("one").count().over("session").alias("session_length"),
                 pl.col("session").n_unique().over("char").alias("n_sessions")
             ]))

def remove_bots(dataf, max_session_hours=24):
    n_rows = max_session_hours*6
    return (dataf
            .filter(pl.col("session_length").max().over("char") < n_rows))