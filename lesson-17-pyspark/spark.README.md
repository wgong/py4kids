[Databricks Sandbox](https://community.cloud.databricks.com)

2019-07-30

reinstall Anaconda
https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart


PREFIX=/home/gong/anaconda3
installing: python-3.7.3-h0371630_0 ...



Apache Spark
http://spark.apache.org/

```
$ mkdir -p ~/spark
$ cd spark
$ tar zxvf ~/Downloads/spark-2.4.3-bin-hadoop2.7.tgz

$ tar zxvf filename.tar.gz -gzipped files
$ tar jxvf filename.tar.bz2 -bzipped files

$ pip install pyspark
```
Successfully built pyspark
Installing collected packages: py4j, pyspark
Successfully installed py4j-0.10.7 pyspark-2.4.3


$ export SPARK_HOME=~/spark
$ pip install findspark

## How to install pyspark
https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart

## Quick Start with pyspark
http://spark.apache.org/docs/latest/quick-start.html

### validate pyspark

### various ways of using pyspark

* pyspark shell
* python <pyspark script>
* spark-submit
* notebook

$ cd ~/spark
$ ./bin/pyspark
Using Python version 3.7.1 (default, Dec 14 2018 19:28:38)
SparkSession available as 'spark'.
```
>>> textFile = spark.read.text("README.md")  # textFile is DataFrame
>>> textFile.take(5)   # Number of rows in this DataFrame
>>> textFile.first()   # First row in this DataFrame

>>> linesWithSpark = textFile.filter(textFile.value.contains("Spark"))  # transform this DataFrame to a new one which contains Spark
>>> linesWithSpark.count()


>>> from pyspark.sql.functions import *   # more on dataset operation
>>> textFile.select(size(split(textFile.value, "\s+")).name("numWords")).agg(max(col("numWords"))).collect()

>>> wordCounts = textFile.select(explode(split(textFile.value, "\s+")).alias("word")).groupBy("word").count()   # different way of counting word
>>> wordCounts.collect()

>>> for k,v in wordCounts.collect():
...     print(k,"\t=>",v)


>>> linesWithSpark.cache()     #  pulling data sets into a cluster-wide in-memory cache

>>> linesWithSpark.count()
>>> linesWithSpark.take(5)
>>> linesWithSpark.collect()
```

$ cd ~/spark/examples/src/main/python

create a wordcount.py

invoke with python after `pip install pyspark`
$ python wordcount.py wordcount.txt

invoke with spark-submit command
$ ~/spark/bin/spark-submit --master local[4] wordcount.py wordcount.txt


19/04/27 18:25:56 INFO DAGScheduler: Job 1 finished: count at NativeMethodAccessorImpl.java:0, took 0.078046 s
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Lines with a: 8, lines with American: 3
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



or 
$ cd ~/spark/examples/src/main/python

$ python pi.py 4

$ python wordcount.py  ../../../../README.md 

$ python wordcount.py  ./data/word_count.text 

$ python sort.py  ./data/word_count.text 


For Python examples, use spark-submit directly:
./bin/spark-submit examples/src/main/python/pi.py


## DataCamp - Apache Spark in Python: Beginner's Guide
https://www.datacamp.com/community/tutorials/apache-spark-python#gs.fMIIqxM


## python-spark-tutorial
https://github.com/jleetutorial/python-spark-tutorial
$ git clone https://github.com/jleetutorial/python-spark-tutorial.git


## DataCamp - Apache Spark Tutorial: ML with PySpark
https://www.datacamp.com/community/tutorials/apache-spark-tutorial-machine-learning


## Spark-py-notebooks
https://github.com/jadianes/spark-py-notebooks
$ git clone https://github.com/jadianes/spark-py-notebooks.git


IPYTHON and IPYTHON_OPTS are removed in Spark 2.0+. Remove these from the environment and set PYSPARK_DRIVER_PYTHON and PYSPARK_DRIVER_PYTHON_OPTS instead.

Support for specifying --pylab on the command line has been removed
Please use `%pylab inline` or `%matplotlib inline` in the notebook itself

gong@gong-desktop:~/spark/tutorials/spark-py-notebooks$ ./run_spark_notebook.sh:
MASTER="spark://127.0.0.1:7077" SPARK_EXECUTOR_MEMORY="4G" PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook" ~/spark/bin/pyspark

Apache Toree is a kernel for the Jupyter Notebook platform providing interactive access to Apache Spark
https://toree.incubator.apache.org/

