import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

glueContext = GlueContext(SparkContext.getOrCreate())

persons = glueContext.create_dynamic_frame.from_catalog(database="legislators", table_name="persons_json")
print("Count: " + str(persons.count()))
persons.printSchema()

memberships = glueContext.create_dynamic_frame.from_catalog(database="legislators", table_name="memberships_json")
print("Count: " + str(memberships.count()))
memberships.printSchema()

orgs = glueContext.create_dynamic_frame.from_catalog(database="legislators", table_name="organizations_json")
print("Count: " + str(orgs.count()))
orgs.printSchema()

orgs = orgs.drop_fields(['other_names','identifiers']).rename_field('id', 'org_id').rename_field('name', 'org_name')
orgs.toDF().show()

memberships.select_fields(['organization_id']).toDF().distinct().show()


l_history = Join.apply(orgs,
                       Join.apply(persons, memberships, 'id', 'person_id'),
                       'org_id', 'organization_id').drop_fields(['person_id', 'org_id'])
print("Count: " + str(l_history.count()))
l_history.printSchema()

glueContext.write_dynamic_frame.from_options(frame = l_history,
              connection_type = "s3",
              connection_options = {"path": "s3://glue-sample-target/output-dir/legislator_history"},
              format = "parquet")

s_history = l_history.toDF().repartition(1)
s_history.write.parquet('s3://glue-sample-target/output-dir/legislator_single')

l_history.toDF().write.parquet('s3://glue-sample-target/output-dir/legislator_part', partitionBy=['org_name'])

dfc = l_history.relationalize("hist_root", "s3://glue-sample-target/temp-dir/")
dfc.keys()

l_history.select_fields('contact_details').printSchema()
dfc.select('hist_root_contact_details').toDF().where("id = 10 or id = 75").orderBy(['id','index']).show()

dfc.select('hist_root').toDF().where("contact_details = 10 or contact_details = 75").select(['id', 'given_name', 'family_name', 'contact_details']).show()

for df_name in dfc.keys():
        m_df = dfc.select(df_name)
        print("Writing to Redshift table: " + df_name)
        glueContext.write_dynamic_frame.from_jdbc_conf(frame = m_df,
                                                       catalog_connection = "redshift3",
                                                       connection_options = {"dbtable": df_name, "database": "testdb"},
                                                       redshift_tmp_dir = "s3://glue-sample-target/temp-dir/")


