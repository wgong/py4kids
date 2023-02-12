## Why 
- blazingly fast - one of the best performing solution
- light-weight
- handles larger than RAM data
- save cost if data size is small to medium (100GB) and no need to launch EMR

## Install
```
pip install polars
```

## Docs

### Polars - Official User Guide	
https://pola-rs.github.io/polars-book/user-guide/introduction.html

### Polars - API Reference Guide	
https://pola-rs.github.io/polars/py-polars/html/reference/index.html

### Polars Source - GitHub
https://github.com/pola-rs/polars

### DB Connector-X

- https://rustrepo.com/repo/sfu-db-connector-x-rust-data-processing

    - [SQLite](https://towardsdatascience.com/connectorx-the-fastest-way-to-load-data-from-databases-a65d4d4062d5)
        - [Connector-X Discussions](https://github.com/sfu-db/connector-x/discussions)
        - https://stackoverflow.com/questions/75307473/how-to-read-a-sqlite-database-file-using-polars-package-in-python


### TPCH benchmark
https://www.pola.rs/benchmarks.html

## Resources: Videos, Blogs, Books

### Polars: Blazingly Fast DataFrames in Rust and Python
https://www.youtube.com/watch?v=kVy3-gMdViM

Databrick Data-AI summit 2022 by Richie Vink	

### Why Polars?	PyData Global 2021 by Richie Vink	
http://youtube.com/watch?v=iwGIuGk5nCE

### Introduction to Polars (2021-03-23)	
https://r-brink.medium.com/introduction-to-polars-ee9e638dc163

### Working with large datasets (300M) on a tiny machine (512MB RAM, 1 core) (2023-01-04)
https://r-brink.medium.com/working-with-large-datasets-300m-on-a-tiny-machine-512mb-ram-1-core-6d1553e474df

Polars is not only blazingly fast on high end hardware, it still performs when you are working on a smaller machine. The results of Pandas show why many organisations and professionals switch to cloud solutions to process larger datasets. Polars show that this is not immediately necessary.	

### Polars: Pandas DataFrame but Much Faster (2023-01-03)
https://towardsdatascience.com/pandas-dataframe-but-much-faster-f475d6be4cd4

### Pandas vs Polar - A look at performance
https://studioterabyte.nl/en/blog/polars-vs-pandas  (2022-07-11)

dataset: https://www.kaggle.com/competitions/nyc-taxi-trip-duration/data?select=train.zip
1.462.644 rows
x25 => 36.566.100 rows (5gb) 

### Replacing Pandas with Polars - A Practical Guide	
https://www.confessionsofadataguy.com/replacing-pandas-with-polars-a-practical-guide/

### Polars — A DataFrame library faster than pandas (2022-12-16)	
https://medium.com/@pyzone.dev/polars-a-dataframe-library-faster-than-pandas-c1267315af0e

### Using the Polars DataFrame Library (2022-11-10)	
https://www.codemag.com/Article/2212051/Using-the-Polars-DataFrame-Library

### 3x times faster Pandas with PyPolars (2021-05-01)	
https://towardsdatascience.com/3x-times-faster-pandas-with-pypolars-7550e605805e

### https://github.com/Jcharis/DataScienceTools/tree/master/PyPolars_Data_Analysis


### Database-like ops benchmark
https://h2oai.github.io/db-benchmark/


- [Polars — A DataFrame library faster than pandas](https://medium.com/@pyzone.dev/polars-a-dataframe-library-faster-than-pandas-c1267315af0e) 2022-12-16
- [Using the Polars DataFrame Library](https://www.codemag.com/Article/2212051/Using-the-Polars-DataFrame-Library) 2022-11-10
- [Lightning-fast queries with Polars](https://www.orchest.io/blog/the-great-python-dataframe-showdown-part-3-lightning-fast-queries-with-polars) 2022-05-25


## Misc

### Tips, Q&A
https://stackoverflow.com/questions/70516702/how-to-assign-exponential-moving-averages-after-groupby-in-python-polars 

#### window functions
https://pola-rs.github.io/polars-book/user-guide/dsl/window_functions.html


https://youtu.be/vjvTD5oTdos


#### Ewm_mean
- https://pola-rs.github.io/polars/py-polars/html/reference/series/api/polars.Series.ewm_mean.html#polars.Series.ewm_mean

- PR: introduce bias parameter to ewm_var and ewm_mean #4636

#### shift
- https://pola-rs.github.io/polars/py-polars/html/reference/dataframe/api/polars.DataFrame.shift.html#polars.DataFrame.shift
- https://stackoverflow.com/questions/73101521/polars-equivalent-to-pandas-groupby-shift

#### diff
- https://pola-rs.github.io/polars/py-polars/html/reference/series/api/polars.Series.diff.html
- https://stackoverflow.com/questions/73273844/how-to-get-the-difference-sets-of-two-polars-dataframes


#### X80 faster
https://www.pola.rs/posts/the-expressions-api-in-polars-is-amazing/

#### Rust vs python
https://able.bio/haixuanTao/data-manipulation-polars-vs-rust--3def44c8


#### Versions
- Python 3.9.13
- polars Version: 0.15.14
- pandas Version: 1.4.4
