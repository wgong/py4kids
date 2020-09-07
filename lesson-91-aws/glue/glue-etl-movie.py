#########################################
### IMPORT LIBRARIES AND SET VARIABLES
#########################################

#Import python modules
from datetime import datetime

#Import pyspark modules
from pyspark.context import SparkContext
import pyspark.sql.functions as f

#Import glue modules
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

#Initialize contexts and session
spark_context = SparkContext.getOrCreate()
glue_context = GlueContext(spark_context)
session = glue_context.spark_session

#Parameters
glue_db = "sampledb"
glue_tbl = "movie_source"
s3_write_path = "s3://wengong-redshift/movies/sink"


#########################################
### EXTRACT (READ DATA)
#########################################

#Log starting time
dt_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Start time:", dt_start)

#Read movie data to Glue dynamic frame
dynamic_frame_read = glue_context.create_dynamic_frame.from_catalog(database = glue_db, table_name = glue_tbl)

#Convert dynamic frame to data frame to use standard pyspark functions
data_frame = dynamic_frame_read.toDF()

#########################################
### TRANSFORM (MODIFY DATA)
#########################################

#Create a decade column from year
decade_col = f.floor(data_frame["year"]/10)*10
data_frame = data_frame.withColumn("decade", decade_col)

#Group by decade: Count movies, get average rating
data_frame_aggregated = data_frame.groupby("decade").agg(
    f.count(f.col("movie_title")).alias('movie_count'),
    f.mean(f.col("rating")).alias('rating_mean'),
)

#Sort by the number of movies per the decade
data_frame_aggregated = data_frame_aggregated.orderBy(f.desc("movie_count"))

#Print result table
#Note: Show function is an action. Actions force the execution of the data frame plan.
#With big data the slowdown would be significant without cacching.
data_frame_aggregated.show(10)

#########################################
### LOAD (WRITE DATA)
#########################################

#Create just 1 partition, because there is so little data
# to avoid too many small files
data_frame_aggregated = data_frame_aggregated.repartition(1)

#Convert back to dynamic frame
dynamic_frame_write = DynamicFrame.fromDF(data_frame_aggregated, glue_context, "dynamic_frame_write")

#Write data back to S3
glue_context.write_dynamic_frame.from_options(
    frame = dynamic_frame_write,
    connection_type = "s3",
    connection_options = {
        "path": s3_write_path,
        #Here you could create S3 prefixes according to a values in specified columns
        #"partitionKeys": ["decade"]
    },
    format = "csv"
)

#Log end time
dt_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Start time:", dt_end)

