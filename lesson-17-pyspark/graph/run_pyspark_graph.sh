cd ~/projects/graph/graph-algo/Graph-Algo-git/notebooks
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS=notebook
pyspark \
--driver-memory 2g \
--executor-memory 6g \
--packages graphframes:graphframes:0.8.1-spark3.0-s_2.12
