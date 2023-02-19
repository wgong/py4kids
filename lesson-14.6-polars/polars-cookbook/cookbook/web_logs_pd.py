import pandas as pd 
def set_types(dataf):
    return (dataf
            .assign(timestamp=lambda d: pd.to_datetime(d['timestamp'], format="%m/%d/%y %H:%M:%S"),
                    guild=lambda d: d['guild'] != -1))
            
def sessionize(dataf, threshold=60*10):
    return (dataf
             .sort_values(["char", "timestamp"])
             .assign(ts_diff=lambda d: (d['timestamp'] - d['timestamp'].shift()).dt.seconds > threshold,
                     char_diff=lambda d: (d['char'].diff() != 0),
                     new_session_mark=lambda d: d['ts_diff'] | d['char_diff'],
                     session=lambda d: d['new_session_mark'].fillna(0).cumsum())
             .drop(columns=['char_diff', 'ts_diff', 'new_session_mark']))

def add_features(dataf):
    return (dataf
              .assign(session_length=lambda d: d.groupby('session')['char'].transform(lambda d: d.count()))
              .assign(n_sessions=lambda d: d.groupby('char')['session'].transform(lambda d: d.nunique())))

def remove_bots(dataf, max_session_hours=24):
    n_rows = max_session_hours*6
    return (dataf
            .assign(max_sess_len=lambda d: d.groupby('char')['session_length'].transform(lambda d: d.max()))
            .loc[lambda d: d["max_sess_len"] < n_rows]
            .drop(columns=["max_sess_len"]))