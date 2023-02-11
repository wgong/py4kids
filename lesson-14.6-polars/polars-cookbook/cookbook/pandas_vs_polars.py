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

import pandas as pd
import polars as pl

from timeit import default_timer
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


COL_WIDTH = {
    "pandas": 15,
    "polars": 15,
    "use-case": 60,
    "datafile": 40,
    "dataset": 15,
}

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


def print_results_table(results):

    # print(results)

    lines = []
    headers = []
    for c in COL_WIDTH.keys():
        headers.append(pad_str(c, width=COL_WIDTH[c], align="center", pad_ch=' '))
    lines.append(headers)

    separators = []
    for c in COL_WIDTH.keys():
        separators.append(pad_str("=", width=COL_WIDTH[c], align="center", pad_ch='='))
    lines.append(separators)

    for use_case in results.keys():
        res = results[use_case]
        row = []
        col_name = "pandas"
        res_col = res.get(col_name, None)
        if res_col is not None:
            col_val = f"{res_col[0]:.6f} {res_col[1]}"
            col_val = pad_str(col_val, width=COL_WIDTH[col_name], align="right", pad_ch=' ')
        else:
            col_val = pad_str("-", width=COL_WIDTH[col_name], align="center", pad_ch='-')
        row.append(col_val)

        col_name = "polars"
        res_col = res.get(col_name, None)
        if res_col is not None:
            col_val = f"{res_col[0]:.6f} {res_col[1]}"
            col_val = pad_str(col_val, width=COL_WIDTH[col_name], align="right", pad_ch=' ')
        else:
            col_val = pad_str("-", width=COL_WIDTH[col_name], align="center", pad_ch='-')
        row.append(col_val)

        col_name = "use-case"
        col_val = pad_str(use_case, width=COL_WIDTH[col_name], align="left", pad_ch=' ')
        row.append(col_val)

        col_name = "datafile"
        res_col = res.get(col_name, "")
        if res_col:
            col_val = pad_str(res_col, width=COL_WIDTH[col_name], align="left", pad_ch=' ')
        else:
            col_val = pad_str("-", width=COL_WIDTH[col_name], align="center", pad_ch='-')
        row.append(col_val)

        col_name = "dataset"
        res_col = res.get(col_name, "")
        if res_col:
            col_val = pad_str(res_col, width=COL_WIDTH[col_name], align="left", pad_ch=' ')
        else:
            col_val = pad_str("-", width=COL_WIDTH[col_name], align="center", pad_ch='-')
        row.append(col_val)
        lines.append(row)

    for row in lines:
        print(" | ".join(row))

#############################################
# define use-case specific functions below
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

def write_out_parquet(lib, datafile, dataset, *args, **kwargs):
    df = read_data(lib, datafile, dataset, *args, **kwargs)
    if df is None: return

    file_out = kwargs.get("file_out", f"../data/{dataset}/{lib}")
    n_factor = kwargs.get("n_factor", 1)

    if n_factor > 1:
        df = df_concat(lib, df, n_factor)
    try:
        Path(file_out).mkdir(parents=True, exist_ok=True)
        if lib == "pandas":
            df.to_parquet(file_out, engine='auto', compression='snappy')
        elif lib == "polars":
            basename = os.path.basename(datafile).split(".")[0]
            suffix = "" if n_factor == 1 else f"-{str(n_factor)}"
            df.write_parquet(f"{file_out}/{basename}{suffix}.parquet")

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

#############################################
def use_case_001(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer() as t:
        print_df_shape(lib, datafile, dataset)
    return t.elapsed, t.unit

def use_case_001a(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer() as t:
        print_df_shape(lib, datafile, dataset)
    return t.elapsed, t.unit

def use_case_002(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer() as t:
        write_out_parquet(lib, datafile, dataset, file_out=f"../data/{dataset}/{lib}")
    return t.elapsed, t.unit

def use_case_002_a(lib, datafile, dataset, n_factor):
    print(f"[ {lib} ]")
    with Timer() as t:
        write_out_parquet(lib, datafile, dataset, file_out=f"../data/{dataset}/{lib}", n_factor=n_factor)
    return t.elapsed, t.unit

def use_case_003(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer() as t:
        print_length_string_in_column(lib, datafile, dataset)
    return t.elapsed, t.unit

def use_case_004(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer() as t:
        convert_trip_duration_to_minutes(lib, datafile, dataset)
    return t.elapsed, t.unit

def use_case_004b(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer() as t:
        convert_trip_duration_to_minutes(lib, datafile, dataset)
    return t.elapsed, t.unit

def use_case_005(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer() as t:
        filter_out_trip_duration_500_seconds(lib, datafile, dataset)
    return t.elapsed, t.unit

def use_case_006(lib, datafile, dataset):
    print(f"[ {lib} ]")
    with Timer() as t:
        filter_group_and_mean(lib, datafile, dataset)
    return t.elapsed, t.unit

############################
# register use-case here
# make sure the referenced function is defined above
############################
RUN_ALL_CASES = True   # run all use-cases 
# RUN_ALL_CASES = False  # run selected use-case where {"active": 1}

USE_CASES = [
    # {
    #     "name": "use_case_001",
    #     "desc": "read_csv and df.shape",
    #     "fn": use_case_001,
    #     "dataset": "uber-ride",
    #     "datafile": "../data/uber-ride/train.csv",
    #     "active": 1,     # dev/debug this one when RUN_ALL_CASES = True; ignored when False
    # },

    {
        "name": "use_case_001a",
        "desc": "read gzipped csv and df.shape",
        "fn": use_case_001,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "use_case_001p",
        "desc": "read_parquet and df.shape",
        "fn": use_case_001,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/polars/train.parquet",
    },

    {
        "name": "use_case_002",
        "desc": "write out parquet",
        "fn": use_case_002,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "use_case_002_a",
        "desc": "read parquet, concat by n_factor, write parquet",
        "fn": use_case_002_a,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/polars/train.parquet",
        "n_factor": 3,
        "active": 1,     # dev/debug this one when RUN_ALL_CASES = True; ignored when False
    },


    {
        "name": "use_case_003",
        "desc": "read_csv and df['id'].str.len()",
        "fn": use_case_003,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "use_case_003_a",
        "desc": "read_parquet and df['id'].str.len()",
        "fn": use_case_003,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/polars/train-3.parquet",
        "active": 1,     # dev/debug this one when RUN_ALL_CASES = True; ignored when False
    },

    {
        "name": "use_case_004",
        "desc": "read_csv and divide trip_duration by 60",
        "fn": use_case_004,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "use_case_004b",
        "desc": "read_parquet and divide trip_duration by 60",
        "fn": use_case_004b,
        "active": 0,     # this case will not run when RUN_ALL_CASES = False
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/polars/train.parquet",
    },


    {
        "name": "use_case_005",
        "desc": "read_csv and filter trip_duration >= 500 sec",
        "fn": use_case_005,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

    {
        "name": "use_case_006",
        "desc": "read_csv and group by and mean",
        "fn": use_case_006,
        "dataset": "uber-ride",
        "datafile": "../data/uber-ride/train.csv.gz",
    },

]

def run_use_cases(cases):
    results = {}
    for use_case in cases:
        # print(use_case)
        try:
            case_name = f"{use_case['name']}: {use_case['desc']}"

            if RUN_ALL_CASES or use_case.get("active", 0):
                print(f"\n## {case_name}")
                results[case_name] = {}
                dataset = use_case.get("dataset","")
                datafile = use_case.get("datafile","")
                results[case_name]["dataset"] = dataset
                results[case_name]["datafile"] = datafile
                if not datafile:
                    print("[Error] datafile missing")
                    continue

                for lib in ["pandas", "polars"]:
                    if use_case['name'] == "use_case_002_a":
                        n_factor = use_case.get("n_factor", 1)
                        results[case_name][lib] = use_case['fn'](lib, datafile, dataset, n_factor)
                    else:
                        results[case_name][lib] = use_case['fn'](lib, datafile, dataset)
        except Exception as e:
            print(f"[ERROR] run_use_cases() \n {str(e)}")                
    return results

def main():
    results = run_use_cases(USE_CASES)
    print_results_table(results)

if __name__ == "__main__":
    main()
  
  
