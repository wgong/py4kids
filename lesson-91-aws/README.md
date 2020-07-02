## [AWS Serverless Workshop](https://github.com/aws-samples/aws-serverless-workshops)

- https://github.com/wgong/aws-serverless-workshops

## [CI/CD FOR SERVERLESS APPLICATIONS](https://cicd.serverlessworkshops.io/)

## Boto 3 Quickstart
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html


## AWS Glue Get Database Tables

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html

```
glue_client = sess.client("glue")

# test
responseGetTables = glue_client.get_tables(DatabaseName="test")
responseGetTables.keys()
responseGetTables['TableList']

# use paginator
database_list = []
StartingToken = None

paginator = glue_client.get_paginator('get_databases')
page_iterator = paginator.paginate(
	PaginationConfig={'PageSize':100, 'StartingToken':StartingToken })

for page in page_iterator:
	for db in page['DatabaseList']:
		database_list.append((db.get('Name', None), db.get('LocationUri', None)))
	try:
		StartingToken = page["NextToken"]
	except KeyError:
		break
```
