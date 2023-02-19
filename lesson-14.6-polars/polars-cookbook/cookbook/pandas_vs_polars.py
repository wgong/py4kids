"""
example sources: 
- https://studioterabyte.nl/en/blog/polars-vs-pandas

- https://towardsdatascience.com/pandas-dataframe-but-much-faster-f475d6be4cd4

- https://github.com/danielbeach/PandasVsPolars
    - Data set: NYC Parking Tickets (42 mil rows x 51 cols)
    - Kaggle Notebook: https://www.kaggle.com/code/travisvoon/polars-demo-by-travis-tang
"""
from pathlib import Path
import os.path
import os

import numpy as np
import pandas as pd
import polars as pl
import connectorx as cx
import urllib
import sqlite3

from datetime import datetime
from timeit import default_timer

TIMER_UNIT = "sec"

# this map config column width in char
COL_WIDTH = {
    "pandas": 11,
    "polars": 11,
    "unit": 4,
    "use-case": 70,
    "datafile": 50,
    "dataset": 15,
}

RSI_PERIOD=100
#############################################
# helper functions
#############################################
# from timer import Timer
class Timer(object):
    CONVERSION = {
            "sec": 1,
            "min": 1/60.0,
            "hr": 1/3600.0, 
            "millisec": 1000, 
            "microsec": 1000000,
        }

    def __init__(self, verbose=False, unit="sec"):
        unit = unit.lower()
        if unit.startswith("mil"): unit = "millisec"
        elif unit.startswith("mic"): unit = "microsec"
        elif unit.startswith("h"): unit = "hr"
        self.unit = unit if unit in ["sec", "min", "hr", "millisec", "microsec"] else "sec"
        self.verbose = verbose
        self.timer = default_timer
        self.elapsed = 0
        
    def __enter__(self):
        self.start = self.timer()
        return self
        
    def __exit__(self,  *args):
        self.elapsed = (self.timer() - self.start) * self.CONVERSION[self.unit]
        if self.verbose:
            print(f'Elapsed time: {self.elapsed:.6f} {self.unit}')

# format string to fixed width
def pad_str(s, width=20, align="center", pad_ch=' '):
    len_s = len(s)
    if len_s > width:
        return s[:width]
    
    pad = (width-len_s)*pad_ch
    if align == "center":
        left = int((width - len_s)/2)*pad_ch
        right = (width - len(left) - len_s)*pad_ch
        s2 = f"{left}{s}{right}"
    elif align == "right":
        s2 = f"{pad}{s}"
    else:
        s2 = f"{s}{pad}"
    return s2


def print_results_table(results, output_csv=True, print_results=False):
    if print_results:
        print(results)

    lines = []
    headers = []
    for c in COL_WIDTH.keys():
        headers.append(pad_str(c, width=COL_WIDTH[c], align="center", pad_ch=' '))
    lines.append(headers)

    separators = []
    for c in COL_WIDTH.keys():
        separators.append(pad_str("=", width=COL_WIDTH[c], align="center", pad_ch='='))
    lines.append(separators)

    data = []
    for case_ in results.keys():
        res = results[case_]
        row = []
        row_data = []
        col_name = "pandas"
        res_col = res.get(col_name, None)
        if res_col is not None:
            col_val = f"{res_col[0]:.6f}"
            row_data.append(col_val)
            col_val = pad_str(col_val, width=COL_WIDTH[col_name], align="right", pad_ch=' ')
        else:
            row_data.append("")
            col_val = pad_str("-", width=COL_WIDTH[col_name], align="center", pad_ch='-')
        row.append(col_val)

        col_name = "polars"
        res_col = res.get(col_name, None)
        if res_col is not None:
            col_val = f"{res_col[0]:.6f}"
            row_data.append(col_val)
            col_val = pad_str(col_val, width=COL_WIDTH[col_name], align="right", pad_ch=' ')
        else:
            row_data.append("")
            col_val = pad_str("-", width=COL_WIDTH[col_name], align="center", pad_ch='-')
        row.append(col_val)

        col_name = "unit"
        row_data.append(TIMER_UNIT)
        col_val = pad_str(TIMER_UNIT, width=COL_WIDTH[col_name], align="right", pad_ch=' ')
        row.append(col_val)

        col_name = "use-case"
        row_data.append(case_)
        col_val = pad_str(case_, width=COL_WIDTH[col_name], align="left", pad_ch=' ')
        row.append(col_val)

        col_name = "datafile"
        res_col = res.get(col_name, "")
        row_data.append(res_col)
        if res_col:
            col_val = pad_str(res_col, width=COL_WIDTH[col_name], align="left", pad_ch=' ')
        else:
            col_val = pad_str("-", width=COL_WIDTH[col_name], align="center", pad_ch='-')
        row.append(col_val)

        col_name = "dataset"
        res_col = res.get(col_name, "")
        row_data.append(res_col)
        if res_col:
            col_val = pad_str(res_col, width=COL_WIDTH[col_name], align="left", pad_ch=' ')
        else:
            col_val = pad_str("-", width=COL_WIDTH[col_name], align="center", pad_ch='-')
        row.append(col_val)
        lines.append(row)

        data.append(row_data)

    # write to console
    for row in lines:
        print(" | ".join(row))

    # write to CSV
    if output_csv:
        basename = os.path.basename(__file__).split(".")[0]
        dt = datetime.now().strftime("%Y-%m-%d_%H-%M")
        file_path = f"{basename}-{dt}.csv"
        # print(f"file_path = {file_path}")
        df = pd.DataFrame(data, columns=list(COL_WIDTH.keys()))
        df.to_csv(file_path, index=False, index_label=False, sep="\t", encoding="utf-8")



#############################################
# define functions shared by all use-cases
#############################################
def read_data(lib, datafile, dataset, *args, **kwargs):
    df = None
    if not Path(datafile).exists():
        print(f"[Error] read_data(): datafile {datafile} not found")
        return df

    if datafile.endswith("csv") or datafile.endswith("csv.gz"):
        if lib == "pandas":
            df = pd.read_csv(datafile)
        elif lib == "polars":
            df = pl.read_csv(datafile)
    elif datafile.endswith("parquet"):
        if lib == "pandas":
            df = pd.read_parquet(datafile, engine='pyarrow')
        elif lib == "polars":
            df = pl.read_parquet(datafile)
    return df

def print_df_shape(lib, datafile, dataset, *args, **kwargs):
    df = read_data(lib, datafile, dataset, *args, **kwargs)
    if df is None: return
    print(df.shape)

def df_concat(lib, df, n_factor):
    """
    Expand df rows by n_factor
    """
    if lib not in ["pandas", "polars"] or df is None:
        return None
    
    df_list = []
    for i in range(n_factor):
        df_list.append(df)
    if lib == "pandas":
        return pd.concat(df_list, ignore_index=True)
    elif lib == "polars":
        return pl.concat(df_list)

def write_out_csv(lib, datafile, dataset, *args, **kwargs):
    df = read_data(lib, datafile, dataset, *args, **kwargs)
    if df is None or lib not in ["pandas","polars"]: return

    out_dir = kwargs.get("out_dir", f"../data/{dataset}/{lib}")
    n_factor = kwargs.get("n_factor", 1)

    if n_factor > 1:
        df = df_concat(lib, df, n_factor)
    try:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        basename = os.path.basename(datafile).split(".")[0]
        suffix = "" if n_factor == 1 else f"-{str(n_factor)}"
        file_path = f"{out_dir}/{basename}{suffix}.csv"

        if lib == "pandas":
            df.to_csv(file_path)
        elif lib == "polars":
            df.write_csv(file_path)

    except Exception as e:
        print(f"[ERROR] write_out_csv({lib}) \n {str(e)}")

def write_out_parquet(lib, datafile, dataset, *args, **kwargs):
    df = read_data(lib, datafile, dataset, *args, **kwargs)
    if df is None: return

    out_dir = kwargs.get("out_dir", f"../data/{dataset}/{lib}")
    n_factor = kwargs.get("n_factor", 1)

    if n_factor > 1:
        df = df_concat(lib, df, n_factor)
    try:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        if lib == "pandas":
            df.to_parquet(out_dir, engine='auto', compression='snappy')
        elif lib == "polars":
            basename = os.path.basename(datafile).split(".")[0]
            suffix = "" if n_factor == 1 else f"-{str(n_factor)}"
            df.write_parquet(f"{out_dir}/{basename}{suffix}.parquet")

    except Exception as e:
        print(f"[ERROR] write_out_parquet({lib}) \n {str(e)}")

def print_length_string_in_column(lib, datafile, dataset, *args, **kwargs):
    df = read_data(lib, datafile, dataset, *args, **kwargs)
    if df is None: return

    try:
        if lib == "pandas":
            df["vendor_id_length"] = df["id"].str.len()
        elif lib == "polars":
            df = df.with_columns(
                [
                    pl.col("id").str.lengths().alias("vendor_id_length")
                ]
            )
        print(df.head())    
    except Exception as e:
        print(f"[ERROR] print_length_string_in_column({lib}) \n {str(e)}")

def convert_trip_duration_to_minutes(lib, datafile, dataset, *args, **kwargs):
    df = read_data(lib, datafile, dataset, *args, **kwargs)
    if df is None: return
    try:
        if lib == "pandas":
            df["trip_duration_minutes"] = df["trip_duration"].apply(
                lambda duration_seconds: duration_seconds / 60
            )
        elif lib == "polars":
            df = df.with_column(
                (pl.col("trip_duration") / 60).alias("trip_duration_minutes")
            )
        print(df.head())
    except Exception as e:
        print(f"[ERROR] convert_trip_duration_to_minutes({lib}) \n {str(e)}")

def filter_out_trip_duration_500_seconds(lib, datafile, dataset, *args, **kwargs):
    df = read_data(lib, datafile, dataset, *args, **kwargs)
    if df is None: return

    cutoff=500
    try:
        if lib == "pandas":
            filtered_df = df[df["trip_duration"] >= cutoff]
        elif lib == "polars":
            filtered_df = df.filter(pl.col("trip_duration") >= cutoff)

        print(filtered_df.shape)
        print(filtered_df.head())
    except Exception as e:
        print(f"[ERROR] filter_out_trip_duration_500_seconds({lib}) \n {str(e)}")

def filter_group_and_mean(lib, datafile, dataset, *args, **kwargs):
    df = read_data(lib, datafile, dataset, *args, **kwargs)
    if df is None: return

    try:
        if lib == "pandas":
            df_mean = df[df["store_and_fwd_flag"] != "Y"]
            df_mean["avg_trip_duration"] = df_mean.groupby(["vendor_id"])["trip_duration"].mean()
            df_mean = df_mean[["vendor_id", "avg_trip_duration"]].dropna(how="any")
        elif lib == "polars":
            df_mean = df.filter(pl.col("store_and_fwd_flag") != "Y")
            df_mean = df_mean.with_columns([
                df_mean.groupby(by="vendor_id").agg([
                    pl.col("trip_duration").mean().alias("avg_trip_duration")
                ])
            ])            # .to_pandas()

        print(df_mean.shape)
        print(df_mean.head())
    except Exception as e:
        print(f"[ERROR] filter_group_and_mean({lib}) \n {str(e)}")

def read_sqlite_write_excel(lib, datafile, dataset, *args, **kwargs):
    query = f"""
    select * from quote_ta_spy where ticker='SPY' order by date_;
    """
    dir_name, base_name = os.path.dirname(datafile), os.path.basename(datafile)
    fname, _ = os.path.splitext(base_name)
    file_path = Path(dir_name) / Path(f"{fname}.xlsx")
    if lib == "pandas":
        conn_ = sqlite3.connect(datafile)
        df = pd.read_sql(query, conn_)
        df.to_excel(file_path, index=False)
    elif lib == "polars":
        root_name = os.getcwd()
        p = Path(root_name) / Path(datafile)
        path = urllib.parse.quote(p.__str__())
        df = cx.read_sql(f"sqlite://{path}", query)
        df.to_excel(file_path, index=False)

def rsi_lepi(df, n=RSI_PERIOD, offset=50):
    """calculate RSI in Pandas
    """
    m = (n-1) / n
    n1 = 1.0 / n
    delta = df['wp'].diff(1)
    gain = delta
    loss = -delta
    with np.errstate(invalid='ignore'):
        gain[(gain<0)|np.isnan(gain)] = 0.0
        loss[(loss<=0)|np.isnan(loss)] = 1e-10 # we don't want divide by zero/NaN
    avg_gain_0 = gain.rolling(window=n).mean()
    avg_loss_0 = loss.rolling(window=n).mean()
    avg_gain_1 = avg_gain_0.shift(periods=1)
    avg_loss_1 = avg_loss_0.shift(periods=1)
    avg_gain = n1*gain + m*avg_gain_1
    avg_loss = n1*loss + m*avg_loss_1
    df['rsi'] = 100 - offset - (100 / (1 + avg_gain / avg_loss)) 
    return df 

def rsi_lepi_lazy(df, n=RSI_PERIOD, offset=50):
    """calculate RSI in Polars lazy API
    """
    n1, m  =  1.0/n, (n-1)/n    
    return (
        df.with_columns([
            pl.col('wp').diff().alias("delta"),
        ])
        .with_columns([
            pl.when(pl.col('delta') > 0).then(pl.col('delta')).otherwise(0).alias("gain"),
            pl.when(pl.col('delta') < 0).then(pl.col('delta')).otherwise(-1e-10).abs().alias("loss"),
        ])
        .with_columns([
            pl.col('gain').rolling_mean(window_size=n).alias("avg_gain_0"),
            pl.col('loss').rolling_mean(window_size=n).alias("avg_loss_0"),
        ])
        .with_columns([
            pl.col('avg_gain_0').shift(periods=1).alias("avg_gain_1"),
            pl.col('avg_loss_0').shift(periods=1).alias("avg_loss_1"),
        ])
        .with_columns([
            (n1*pl.col('gain') + m*pl.col('avg_gain_1')).alias("avg_gain"),
            (n1*pl.col('loss') + m*pl.col('avg_loss_1')).alias("avg_loss"),
        ])
        .with_columns([
            (100 - offset - (100 / (1 + pl.col('avg_gain')/pl.col('avg_loss') ))).alias("rsi"),
        ])
        .drop([
            'delta', 'gain', 'loss', 'avg_gain_0', 'avg_loss_0', 'avg_gain_1', 'avg_loss_1', 'avg_gain', 'avg_loss'
        ])
    )

def read_sqlite_calc_rsi(lib, datafile, dataset, *args, **kwargs):
    query = f"""
    select * from quote_ta_spy where ticker='SPY' order by date_;
    """
    dir_name, base_name = os.path.dirname(datafile), os.path.basename(datafile)
    fname, _ = os.path.splitext(base_name)
    file_path = Path(dir_name) / Path(f"{fname}-rsi-{lib}.csv")
    if lib == "pandas":
        # read
        conn_ = sqlite3.connect(datafile)
        df = pd.read_sql(query, conn_)
        # calc
        df = df[["date_","wp","rsi"]]
        df.rename(columns={"rsi":"rsi_old"}, inplace=True)
        df = rsi_lepi(df)
        # write
        df.to_csv(file_path, index=False)
    elif lib == "polars":
        # read
        root_name = os.getcwd()
        p = Path(root_name) / Path(datafile)
        path = urllib.parse.quote(p.__str__())
        df = cx.read_sql(f"sqlite://{path}", query)
        # calc
        df = df[["date_","wp","rsi"]]
        df.rename(columns={"rsi":"rsi_old"}, inplace=True)
        df = pl.from_pandas(df).lazy()  # convert to df in polars
        df = df.pipe(rsi_lepi_lazy).collect()
        # write
        df.write_csv(file_path)


def analyze_web_logs(lib, datafile, dataset, *args, **kwargs):
    # great tutorial
    # https://calmcode.io/polars/introduction.html
    # https://gist.github.com/koaning/5a0f3f27164859c42da5f20148ef3856#comments
    #  pandas: 537.280766 s
    #  polars:   9.236657 s
    if lib == "pandas":
        from web_logs_pd import set_types, sessionize, add_features, remove_bots
        df = pd.read_csv(datafile)
        print(f"lib: {lib}, shape={df.shape}")
        df.columns = [c.replace(" ", "") for c in df.columns]
        dataf = df.pipe(set_types).pipe(sessionize)
        final = dataf.pipe(add_features).pipe(remove_bots)
    elif lib == "polars":
        from web_logs_pl import set_types, sessionize, add_features, remove_bots
        df = pl.read_csv(datafile, parse_dates=False, n_threads=10)
        df.columns = [c.replace(" ", "") for c in df.columns]
        df = df.lazy()
        print(f"lib: {lib}, shape={df.collect().shape}")
        (df.pipe(set_types)
            .pipe(sessionize)
            .pipe(add_features)
            .pipe(remove_bots)
            .collect())
        
    

#############################################
# declare case_xxx functions
#############################################
def case_001(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        print_df_shape(lib, datafile, dataset)
    return t.elapsed, t.unit

def case_001a(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        print_df_shape(lib, datafile, dataset)
    return t.elapsed, t.unit

def case_002(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        write_out_parquet(lib, datafile, dataset, out_dir=f"../data/{dataset}/{lib}")
    return t.elapsed, t.unit

def case_002a(lib, datafile, dataset, n_factor):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        write_out_parquet(lib, datafile, dataset, out_dir=f"../data/{dataset}/{lib}", n_factor=n_factor)
    return t.elapsed, t.unit

def case_003(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        print_length_string_in_column(lib, datafile, dataset)
    return t.elapsed, t.unit

def case_004(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        convert_trip_duration_to_minutes(lib, datafile, dataset)
    return t.elapsed, t.unit

def case_004b(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        convert_trip_duration_to_minutes(lib, datafile, dataset)
    return t.elapsed, t.unit

def case_005(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        filter_out_trip_duration_500_seconds(lib, datafile, dataset)
    return t.elapsed, t.unit

def case_006(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        filter_group_and_mean(lib, datafile, dataset)
    return t.elapsed, t.unit

def case_007(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        read_sqlite_write_excel(lib, datafile, dataset)
    return t.elapsed, t.unit

def case_008(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        read_sqlite_calc_rsi(lib, datafile, dataset)
    return t.elapsed, t.unit

def case_009(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer(unit=TIMER_UNIT) as t:
        analyze_web_logs(lib, datafile, dataset)
    return t.elapsed, t.unit



############################
# register use-case here
# make sure the referenced function is defined above
############################
RUN_ALL_CASES = True   # run all use-cases 
RUN_ALL_CASES = False  # run selected use-case where {"active": 1}

CASE_MAP = [
    # {
    #     "name": "case_001",
    #     "desc": "read_csv and df.shape",
    #     "fn": case_001,
    #     "dataset": "uber-ride",
    #     "datafile": "../data/uber-ride/train.csv",
    #     "active": 1,     # dev/debug this one when RUN_ALL_CASES = True; ignored when False
    # },

    {
        "name": "case_001a",
        "desc": "read gzipped csv and df.shape",
        "fn": case_001,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
        "data_url": None,
    },

    {
        "name": "case_001p",
        "desc": "read parquet and df.shape",
        "fn": case_001,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/polars/train.parquet",
    },

    {
        "name": "case_002",
        "desc": "write parquet",
        "fn": case_002,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "case_002a",
        "desc": "read parquet, concat by n_factor, write parquet",
        "fn": case_002a,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/polars/train.parquet",
        "n_factor": 3,
        "active": 0,     # dev/debug this one when RUN_ALL_CASES = True; ignored when False
    },


    {
        "name": "case_003",
        "desc": "read csv and df['id'].str.len()",
        "fn": case_003,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "case_003a",
        "desc": "read parquet and df['id'].str.len()",
        "fn": case_003,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/polars/train-3.parquet",
    },

    {
        "name": "case_004",
        "desc": "read csv and divide trip_duration by 60",
        "fn": case_004,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "case_004b",
        "desc": "read parquet and divide trip_duration by 60",
        "fn": case_004b,
        "active": 0,     # this case will not run when RUN_ALL_CASES = False
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/polars/train.parquet",
    },


    {
        "name": "case_005",
        "desc": "read csv and filter trip_duration >= 500 sec",
        "fn": case_005,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "case_006",
        "desc": "read csv and group by and mean",
        "fn": case_006,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "case_007",
        "desc": "read sqlite and write excel",
        "fn": case_007,
        "dataset": "spy",
        "datafile": "../data/spy/spy.sqlite",
    },

    {
        "name": "case_008",
        "desc": "calculate RSI",
        "fn": case_008,
        "dataset": "spy",
        "datafile": "../data/spy/spy.sqlite",
        "active": 0,     # dev/debug this one when RUN_ALL_CASES = True; ignored when False
    },

    {
        "name": "case_009",
        "desc": "analyze web logs",
        "fn": case_009,
        "dataset": "kaggle",
        "datafile": "../data/kaggle/wowah_data.csv",
        "data_url": "https://www.kaggle.com/datasets/mylesoneill/warcraft-avatar-history",
        "active": 1,     # dev/debug this one when RUN_ALL_CASES = True; ignored when False
    },

]

def main():
    results = {}
    for case_ in CASE_MAP:
        # print(case_)
        try:
            case_name = f"{case_['name']}: {case_['desc']}"

            if RUN_ALL_CASES or case_.get("active", 0):
                print(f"\n## {case_name}")
                results[case_name] = {}
                dataset = case_.get("dataset","")
                datafile = case_.get("datafile","")
                results[case_name]["dataset"] = dataset
                results[case_name]["datafile"] = datafile
                if not datafile:
                    print("[Error] datafile missing")
                    continue

                for lib in ["pandas", "polars"]:
                    try:
                        if case_['name'] == "case_002a":
                            n_factor = case_.get("n_factor", 1)
                            results[case_name][lib] = case_['fn'](lib, datafile, dataset, n_factor)
                        else:
                            results[case_name][lib] = case_['fn'](lib, datafile, dataset)
                    except Exception as e:
                        print(f"[ERROR] lib={lib} \n {str(e)}")                
                        continue

        except Exception as e:
            print(f"[ERROR] case={case_} \n {str(e)}")                
            continue

    print_results_table(results)

if __name__ == "__main__":
    main()