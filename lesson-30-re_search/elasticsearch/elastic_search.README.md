How To Install and Configure Elasticsearch on Ubuntu 20.04
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-20-04



### Install
```
$ curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
$ echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
$ sudo apt update
$ sudo apt install elasticsearch

```

### Config

sudo vi /etc/elasticsearch/elasticsearch.yml

change
network.host: localhost

sudo systemctl status elasticsearch
sudo systemctl start elasticsearch

sudo systemctl enable elasticsearch  # to enable auto-start at boot


### Test

curl -XGET 'http://localhost:9200'                # a quick check
curl -XGET 'http://localhost:9200/_nodes?pretty'   # a more thorough check

- create
curl -XPOST -H "Content-Type: application/json" 'http://localhost:9200/tutorial/helloworld/1' -d '{ "message": "Hello World!" }'

- query
curl -XGET -H "Content-Type: application/json" 'http://localhost:9200/tutorial/helloworld/1' 

- update
curl -X PUT -H "Content-Type: application/json"  'localhost:9200/tutorial/helloworld/1?pretty' -d '
{
  "message": "Hello, People!"
}'


### Tutorial

#### pip install elasticsearch

### Docs

[Elasticsearch API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html)


#### Search multiple docs in one request

```
# create an index
$ curl -X PUT -H "Content-Type: application/json"  'localhost:9200/test_index'

$ curl -X PUT -H "Content-Type: application/json"  'localhost:9200/test_index/_mapping' -d '
{
  "properties": {
    "code": {
        "type": "string"
    }
  }
}
'

$ curl -X PUT -H "Content-Type: application/json"  'localhost:9200/test_index/_mapping' -d '
{
  "properties": {
    "date_of_birth": {
      "type": "date",
      "format": "dd/MM/yyyy"
    }
  }
}
'

$ curl -X POST -H "Content-Type: application/json"  'localhost:9200/test_index/_bulk' -d '
{"index":{"_index":"test_index","_type":"doc","_id":1}}
{"code":"0Qr7EjzE943Q"}
{"index":{"_index":"test_index","_type":"doc","_id":2}}
{"code":"GsPVbMMbVr4s"}
'

$ curl -X POST -H "Content-Type: application/json"  'localhost:9200/test_index/_search' -d '
{
    "query": {
        "terms": {
           "code": [
              "0Qr7EjzE943Q",
              "GsPVbMMbVr4s"
           ]
        }
    }
}
'

```