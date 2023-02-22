# Compare polars vs pandas

Explore how polars and pandas process data differently

```
python pandas_vs_polars.py
```
results are printed to console and save to a CSV (e.g. pandas_vs_polars-2023-02-22_14-50.csv)

## Configure which case to run

`RUN_ALL_CASES`  |  `CASE_MAP.active` | action
  True  | 0 | skip
  True  | * | run
  False | * | skip
  False | 1 | run


## case_009: analyze web logs
[ pandas ]
lib: pandas, shape=(10826734, 7)
[ polars ]
lib: polars, shape=(10826734, 7)
  pandas    |   polars    | unit |                                use-case                                |                      datafile                      |     dataset    
=========== | =========== | ==== | ====================================================================== | ================================================== | ===============
 647.730754 |   10.379160 |  sec | case_009: analyze web logs                                             | ../data/kaggle/wowah_data.csv                      | kaggle       