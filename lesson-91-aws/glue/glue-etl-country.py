import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [TempDir, JOB_NAME]
args = getResolvedOptions(sys.argv, ['TempDir','JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
## @type: DataSource
## @args: [database = "sampledb", table_name = "wdi_country", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "sampledb", table_name = "wdi_country", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("country code", "string", "country code", "string"), ("short name", "string", "short name", "string"), ("table name", "string", "table name", "string"), ("long name", "string", "long name", "string"), ("2-alpha code", "string", "2-alpha code", "string"), ("currency unit", "string", "currency unit", "string"), ("special notes", "string", "special notes", "string"), ("region", "string", "region", "string"), ("income group", "string", "income group", "string"), ("wb-2 code", "string", "wb-2 code", "string"), ("national accounts base year", "string", "national accounts base year", "string"), ("national accounts reference year", "string", "national accounts reference year", "string"), ("sna price valuation", "string", "sna price valuation", "string"), ("lending category", "string", "lending category", "string"), ("other groups", "string", "other groups", "string"), ("system of national accounts", "string", "system of national accounts", "string"), ("alternative conversion factor", "string", "alternative conversion factor", "string"), ("ppp survey year", "string", "ppp survey year", "string"), ("balance of payments manual in use", "string", "balance of payments manual in use", "string"), ("external debt reporting status", "string", "external debt reporting status", "string"), ("system of trade", "string", "system of trade", "string"), ("government accounting concept", "string", "government accounting concept", "string"), ("imf data dissemination standard", "string", "imf data dissemination standard", "string"), ("latest population census", "string", "latest population census", "string"), ("latest household survey", "string", "latest household survey", "string"), ("source of most recent income and expenditure data", "string", "source of most recent income and expenditure data", "string"), ("vital registration complete", "string", "vital registration complete", "string"), ("latest agricultural census", "string", "latest agricultural census", "string"), ("latest industrial data", "long", "latest industrial data", "long"), ("latest trade data", "long", "latest trade data", "long")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("country code", "string", "country code", "string"), ("short name", "string", "short name", "string"), ("table name", "string", "table name", "string"), ("long name", "string", "long name", "string"), ("2-alpha code", "string", "2-alpha code", "string"), ("currency unit", "string", "currency unit", "string"), ("special notes", "string", "special notes", "string"), ("region", "string", "region", "string"), ("income group", "string", "income group", "string"), ("wb-2 code", "string", "wb-2 code", "string"), ("national accounts base year", "string", "national accounts base year", "string"), ("national accounts reference year", "string", "national accounts reference year", "string"), ("sna price valuation", "string", "sna price valuation", "string"), ("lending category", "string", "lending category", "string"), ("other groups", "string", "other groups", "string"), ("system of national accounts", "string", "system of national accounts", "string"), ("alternative conversion factor", "string", "alternative conversion factor", "string"), ("ppp survey year", "string", "ppp survey year", "string"), ("balance of payments manual in use", "string", "balance of payments manual in use", "string"), ("external debt reporting status", "string", "external debt reporting status", "string"), ("system of trade", "string", "system of trade", "string"), ("government accounting concept", "string", "government accounting concept", "string"), ("imf data dissemination standard", "string", "imf data dissemination standard", "string"), ("latest population census", "string", "latest population census", "string"), ("latest household survey", "string", "latest household survey", "string"), ("source of most recent income and expenditure data", "string", "source of most recent income and expenditure data", "string"), ("vital registration complete", "string", "vital registration complete", "string"), ("latest agricultural census", "string", "latest agricultural census", "string"), ("latest industrial data", "long", "latest industrial data", "long"), ("latest trade data", "long", "latest trade data", "long")], transformation_ctx = "applymapping1")
## @type: ResolveChoice
## @args: [choice = "make_cols", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_cols", transformation_ctx = "resolvechoice2")
## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")
## @type: DataSink
## @args: [catalog_connection = "redshiftc1db", connection_options = {"dbtable": "wdi_country", "database": "wdi"}, redshift_tmp_dir = TempDir, transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = dropnullfields3]
datasink4 = glueContext.write_dynamic_frame.from_jdbc_conf(frame = dropnullfields3, catalog_connection = "redshiftc1db", connection_options = {"dbtable": "wdi_country", "database": "wdi"}, redshift_tmp_dir = args["TempDir"], transformation_ctx = "datasink4")
job.commit()
