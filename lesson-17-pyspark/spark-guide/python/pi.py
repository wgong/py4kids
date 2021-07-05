#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import print_function

import sys
from random import random
from operator import add
import time
import math

from pyspark.sql import SparkSession

def help():
    return f"""
    Usage:
        $ python {__file__} [partitions] [samples]
    or
        $ spark-submit {__file__} [partitions] [samples]

    """

if __name__ == "__main__":
    """
        Usage: pi [partitions] [samples]
    """

    try:
        partitions = int(sys.argv[1]) if len(sys.argv) > 1 else 2
        samples    = int(sys.argv[2]) if len(sys.argv) > 2 else 1000000
    except:
        print(help())
        sys.exit(-1)


    spark = SparkSession\
        .builder\
        .appName("PythonPi")\
        .getOrCreate()

    n = samples * partitions

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    t1 = time.time_ns()
    count = spark.sparkContext\
        .parallelize(range(1, n + 1), partitions)\
        .map(f)\
        .reduce(add)
    t2 = time.time_ns()
    pi_val = 4.0 * count / n
    print(f"Pi is roughly {pi_val:.8f} vs math.pi = {math.pi} [completed in {(t2-t1)/1.0E9} sec]")

    spark.stop()
    sys.exit(0)