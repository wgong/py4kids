
## pretty curl
- https://stackoverflow.com/questions/15814220/elastic-search-make-pretty-format-as-the-default

add 
```curl() { `which curl` $@ | python -mjson.tool ; } ```
or
```alias pp='python -mjson.tool'```
 to .bashrc

## [42 Elasticsearch Query Examples](https://coralogix.com/log-analytics-blog/42-elasticsearch-query-examples-hands-on-tutorial/)

```
# return all docs
$ curl -X GET http://localhost:9200/_search | pp

# create index
$ curl -X PUT 'localhost:9200/employees'

# query
$ curl -X GET 'localhost:9200/employees'

# create a mapping
$ curl -X PUT 'localhost:9200/employees/_mapping' -H "Content-Type: application/json" -d '
{
  "properties": {
    "date_of_birth": {
      "type": "date",
      "format": "dd/MM/yyyy"
    }
  }
}
'

# bulk load
$ curl -X POST 'localhost:9200/employees/_bulk' -H "Content-Type: application/json" -d '
{ "index" : { "_index" : "employees", "_id" : "1" } }
{"id":1,"name":"Huntlee Dargavel","email":"hdargavel0@japanpost.jp","gender":"male","ip_address":"58.11.89.193","date_of_birth":"11/09/1990","company":"Talane","position":"Research Associate","experience":7,"country":"China","phrase":"Multi-channelled coherent leverage","salary":180025}
{ "index" : { "_index" : "employees", "_id" : "2" } }
{"id":2,"name":"Othilia Cathel","email":"ocathel1@senate.gov","gender":"female","ip_address":"3.164.153.228","date_of_birth":"22/07/1987","company":"Edgepulse","position":"Structural Engineer","experience":11,"country":"China","phrase":"Grass-roots heuristic help-desk","salary":193530}
{ "index" : { "_index" : "employees", "_id" : "3" } }
{"id":3,"name":"Winston Waren","email":"wwaren2@4shared.com","gender":"male","ip_address":"202.37.210.94","date_of_birth":"10/11/1985","company":"Yozio","position":"Human Resources Manager","experience":12,"country":"China","phrase":"Versatile object-oriented emulation","salary":50616}
{ "index" : { "_index" : "employees", "_id" : "4" } }
{"id" : 4,"name" : "Alan Thomas","email" : "athomas2@example.com","gender" : "male","ip_address" : "200.47.210.95","date_of_birth" : "11/12/1985","company" : "Yamaha","position" : "Resources Manager","experience" : 12,"country" : "China","phrase" : "Emulation of roots heuristic coherent systems","salary" : 300000}
'

$ curl -X GET 'localhost:9200/employees/_count'

$ curl -X GET 'localhost:9200/employees/_doc/1?pretty'


1. Match Query 
- search docs containing the word “heuristic” in the “phrase” field

The “match” query is one of the most basic and commonly used queries in Elasticsearch and functions as a full-text query. We can use this query to search for text, numbers or boolean values.

$ curl -X POST -H "Content-Type: application/json"  'localhost:9200/employees/_search' -d '
{
    "query": {
        "match": {
           "phrase": {
                "query" : "heuristic"
            }
        }
    }
}
'

$ curl -X POST -H "Content-Type: application/json"  'localhost:9200/employees/_search' -d '
{
    "query": {
        "match": {
           "phrase": {
                "query" : "heuristic roots help"
            }
        }
    }
}
' | pp


$ curl -X POST -H "Content-Type: application/json"  'localhost:9200/employees/_search' -d '
{
    "query": {
        "match": {
           "phrase": {
                "query" : "heuristic roots help",
                "operator": "AND"
            }
        }
    }
}
' | pp


$ curl -X POST -H "Content-Type: application/json"  'localhost:9200/employees/_search' -d '
{
    "query": {
        "terms": {
           "gender": [
                "female",
                "male"
            ]
        }
    }
}
' | pp

$ curl -X POST -H "Content-Type: application/json"  'localhost:9200/employees/_search' -d '
{
    "query": {
        "terms": {
           "ip_address": [
               "202.37.210.94",
                "200.47.210.95"
            ]
        }
    }
}
' | pp



```