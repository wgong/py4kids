"""
examples from 
https://studioterabyte.nl/en/blog/polars-vs-pandas

"""

import pandas as pd
import polars as pl
from timer import Timer

def print_results(results):
    print(f"     Pandas     |    Polars     |    Use-case Name ")
    print(f"  {13*'='} | {13*'='} | {50*'='} ")
    for use_case in results.keys():
        res = results[use_case]
        out_str = ""
        res_pd = res.get('pandas', None)
        if res_pd is not None:
            out_str += f"  {res_pd[0]:.6f} {res_pd[1]}  |"
        else:
            out_str += f"  {13*'-'} |"
        res_pl = res.get('polars', None)
        if res_pl is not None:
            out_str += f"  {res_pl[0]:.6f} {res_pl[1]} |"
        else:
            out_str += f" {13*'-'} |"
        
        out_str += f"  {use_case}"
        print(out_str)


#############################################
# define use-case specific functions below
#############################################
def read_csv_df(lib, test_file="../data/train/train.csv"):
    if lib == "pandas":
        df = pd.read_csv(test_file)
    elif lib == "polars":
        df = pl.read_csv(test_file)
    else:
        df = None
    return df
 
def print_df_shape(lib):
    df = read_csv_df(lib)
    if df is None: return
    print(df.shape)

def print_length_string_in_column(lib):
    df = read_csv_df(lib)
    if df is None: return

    try:
        if lib == "pandas":
            df["vendor_id_length"] = df["id"].str.len()
        elif lib == "polars":
            df = df.with_columns(
                [
                    pl.col("id").str.lengths().alias("vendor_id_length")
                ]
            ).to_pandas()
        print(df.head())    
    except Exception as e:
        print(f"[ERROR] print_length_string_in_column() \n {str(e)}")

def convert_trip_duration_to_minutes(lib):
    df = read_csv_df(lib)
    if df is None: return

    try:
        if lib == "pandas":
            df["trip_duration_minutes"] = df["trip_duration"].apply(
                lambda duration_seconds: duration_seconds / 60
            )
        elif lib == "polars":
            df = df.with_column(
                (pl.col("trip_duration") / 60).alias("trip_duration_minutes")
            ).to_pandas()
        print(df.head())
    except Exception as e:
        print(f"[ERROR] convert_trip_duration_to_minutes() \n {str(e)}")

def filter_out_trip_duration_500_seconds(lib, cutoff=500):
    df = read_csv_df(lib)
    if df is None: return

    try:
        if lib == "pandas":
            filtered_df = df[df["trip_duration"] >= cutoff]
        elif lib == "polars":
            filtered_df = df.filter(pl.col("trip_duration") >= cutoff).to_pandas()

        print(filtered_df.shape)
        print(filtered_df.head())
    except Exception as e:
        print(f"[ERROR] filter_out_trip_duration_500_seconds() \n {str(e)}")

def filter_group_and_mean(lib):
    df = read_csv_df(lib)
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
            ]).to_pandas()

        print(df_mean.shape)
        print(df_mean.head())
    except Exception as e:
        print(f"[ERROR] filter_group_and_mean() \n {str(e)}")
#############################################
def use_case_001(lib):
    print(f"[ {lib} ]")
    with Timer() as t:
        print_df_shape(lib)
    return t.elapsed, t.unit

def use_case_003(lib):
    print(f"[ {lib} ]")
    with Timer() as t:
        print_length_string_in_column(lib)
    return t.elapsed, t.unit

def use_case_004(lib):
    print(f"[ {lib} ]")
    with Timer() as t:
        convert_trip_duration_to_minutes(lib)
    return t.elapsed, t.unit

def use_case_005(lib):
    print(f"[ {lib} ]")
    with Timer() as t:
        filter_out_trip_duration_500_seconds(lib, cutoff=500)
    return t.elapsed, t.unit

def use_case_006(lib):
    print(f"[ {lib} ]")
    with Timer() as t:
        filter_group_and_mean(lib)
    return t.elapsed, t.unit

############################
# register use-case here
# make sure the referenced function is defined above
############################
USE_CASES = [
    {
        "name": "use_case_001",
        "desc": "read_csv and df.shape",
        "fn": use_case_001,
        "active": 1
    },

    {
        "name": "use_case_003",
        "desc": "read_csv and df['id'].str.len()",
        "fn": use_case_003,
        "active": 1
    },

    {
        "name": "use_case_004",
        "desc": "read_csv and divide trip_duration by 60",
        "fn": use_case_004,
        "active": 1
    },

    {
        "name": "use_case_005",
        "desc": "read_csv and filter trip_duration >= 500 sec",
        "fn": use_case_005,
        "active": 1
    },

    {
        "name": "use_case_006",
        "desc": "read_csv and group by and mean",
        "fn": use_case_006,
        "active": 1
    },

]

def perform_use_cases(cases):
    results = {}
    for use_case in cases:
        try:
            case_name = f"{use_case['name']}: {use_case['desc']}"
            if not use_case.get("active", 0): continue

            print(f"\n## {case_name}")
            results[case_name] = {}
            for lib in ["pandas", "polars"]:
                results[case_name][lib] = use_case['fn'](lib)
        except Exception as e:
            print(f"[ERROR] perform_use_cases() \n {str(e)}")                
    return results

def main():
    results = perform_use_cases(USE_CASES)
    # print(results)
    print_results(results)

if __name__ == "__main__":
    main()
  
  
