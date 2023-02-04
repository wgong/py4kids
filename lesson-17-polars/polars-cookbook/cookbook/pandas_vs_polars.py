"""
examples from 
https://studioterabyte.nl/en/blog/polars-vs-pandas

"""

from time import time
import pandas as pd
import polars as pl

name_dic = {"pl": "polars", "pd": "pandas"}

def generate_df(lib, test_file="../data/train/train.csv"):
    if lib == "pd":
        df = pd.read_csv(test_file)
    elif lib == "pl":
        df = pl.read_csv(test_file)
    else:
        df = None
    return df
 
def print_df_shape(lib):
    df = generate_df(lib)
    if df is not None:
        print(df.shape)


def print_length_string_in_column(lib):
    df = generate_df(lib)
    if df is not None:
        if lib == "pd":
            df["vendor_id_length"] = df["id"].str.len()
        elif lib == "pl":
            df = df.with_columns(
                [
                    pl.col("id").str.lengths().alias("vendor_id_length")
                ]
            )
        print(df.head())    

def convert_trip_duration_to_minutes(lib):
 
    df = generate_df(lib)
    if df is not None:
        if lib == "pd":
            df["trip_duration_minutes"] = df["trip_duration"].apply(
                lambda duration_seconds: duration_seconds / 60
            )
        elif lib == "pl":
            df = df.with_column(
                (pl.col("trip_duration") / 60).alias("trip_duration_minutes")
            )
        print(df.head())

def filter_out_trip_duration_500_seconds(lib, cutoff=500):
    df = generate_df(lib)
    if df is not None:
        if lib == "pd":
            filtered_df = df[df["trip_duration"] >= cutoff]
        elif lib == "pl":
            filtered_df = df.filter(pl.col("trip_duration") >= cutoff)

        print(filtered_df.shape)
        print(filtered_df.head())

def filter_group_and_mean(lib):
    df = generate_df(lib)
    if df is not None:
        if lib == "pd":
            df_mean = df[df["store_and_fwd_flag"] != "Y"]
            df_mean["avg_trip_duration"] = df_mean.groupby(["vendor_id"])["trip_duration"].mean()
            df_mean = df_mean[["vendor_id", "avg_trip_duration"]].dropna(how="any")
        elif lib == "pl":
            df_mean = df.filter(pl.col("store_and_fwd_flag") != "Y")
            df_mean = df_mean.with_columns([
                df_mean.groupby(by="vendor_id").agg([
                    pl.col("trip_duration").mean().alias("avg_trip_duration")
                ])
            ])
    
        print(df_mean.shape)
        print(df_mean.head())

def use_case_01(lib):
    """
    ## use_case_01: read_csv and df.shape
    [ pandas ]
    (1458644, 11)
    Completed in 3.402884 sec

    [ polars ]
    (1458644, 11)
    Completed in 0.331881 sec
    """
    # Start the time
    start_time = time()
    lib_name = name_dic.get(lib,"")
    print(f"[ {lib_name} ]")

    print_df_shape(lib)

    # End the timer
    end_time = time()
    # Print the elapsed time in seconds
    print(f"Completed in {(end_time - start_time):.6f} sec\n")


def use_case_03(lib):
    """
    """
    # Start the time
    start_time = time()
    lib_name = name_dic.get(lib,"")
    print(f"[ {lib_name} ]")

    print_length_string_in_column(lib)

    # End the timer
    end_time = time()
    # Print the elapsed time in seconds
    print(f"Completed in {(end_time - start_time):.6f} sec\n")

def use_case_04(lib):
    """
    """
    # Start the time
    start_time = time()
    lib_name = name_dic.get(lib,"")
    print(f"[ {lib_name} ]")

    convert_trip_duration_to_minutes(lib)

    # End the timer
    end_time = time()
    # Print the elapsed time in seconds
    print(f"Completed in {(end_time - start_time):.6f} sec\n")

def use_case_05(lib):
    """
    """
    # Start the time
    start_time = time()
    lib_name = name_dic.get(lib,"")
    print(f"[ {lib_name} ]")

    filter_out_trip_duration_500_seconds(lib, cutoff=500)

    # End the timer
    end_time = time()
    # Print the elapsed time in seconds
    print(f"Completed in {(end_time - start_time):.6f} sec\n")

def use_case_06(lib):
    """
    """
    # Start the time
    start_time = time()
    lib_name = name_dic.get(lib,"")
    print(f"[ {lib_name} ]")

    filter_group_and_mean(lib)

    # End the timer
    end_time = time()
    # Print the elapsed time in seconds
    print(f"Completed in {(end_time - start_time):.6f} sec\n")

def perform_use_cases(cases):
    for case in cases:
        if case == "01":
            print("\n## use_case_01: read_csv and df.shape")
            for lib in ["pd", "pl"]:
                use_case_01(lib)

        elif case == "03":
            print("\n## use_case_03: read_csv and df['id'].str.len()")
            for lib in ["pd", "pl"]:
                use_case_03(lib)

        elif case == "04":
            print("\n## use_case_04: read_csv and divide trip_duration by 60")
            for lib in ["pd", "pl"]:
                use_case_04(lib)

        elif case == "05":
            print("\n## use_case_05: read_csv and filter trip_duration >= 500 sec")
            for lib in ["pd", "pl"]:
                use_case_05(lib)

        elif case == "06":
            print("\n## use_case_06: read_csv and group by and mean")
            for lib in ["pd", "pl"]:
                use_case_06(lib)

def main():
   # Perform one of the above described use cases
   cases = ["01", "03", "04", "05",
        "06"]
   perform_use_cases(cases)
 
 
if __name__ == "__main__":
  
   # Call main function to perform use case
   main()
  
  
