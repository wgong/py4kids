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


### Docs

[Elasticsearch API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html)