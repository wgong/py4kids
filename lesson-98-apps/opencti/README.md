# VirtualBox Setup

https://www.notion.so/luatix/Virtual-machine-template-1789b4442b414dbf87f748db51c85aa5


into ~/Downloads/Dad/openCTI/


remove virtualbox v5.2.22 and install v6.0.22
https://askubuntu.com/questions/703746/how-to-completely-remove-virtualbox




https://www.tecmint.com/install-virtualbox-guest-additions-in-ubuntu/

# Docker Setup
https://www.notion.so/Using-Docker-03d5c0592b9d4547800cc9f4ff7be2b8

use https://www.uuidgenerator.net/version4 to generate uuid4 strings to set "ChangeMe" in .env file

git clone https://github.com/OpenCTI-Platform/docker.git


## install docker and docker-compose on Ubuntu 16.04
https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=94798094


```
$ sudo systemctl status docker  ##  check docker status

$ docker --version
## Docker version 19.03.12, build 48a66213fe

$ docker run hello-world  ##  test docker

$ docker-compose --version
## docker-compose version 1.17.0, build ac53b73

$ env $(cat .env | grep ^[A-Z] | xargs) docker stack deploy --compose-file docker-compose.yml opencti
## above not working

```

### Start OpenCTI docker

```
$ env $(cat .env | grep ^[A-Z] | xargs) sudo docker-compose up

```
start = 22.36, stop = 22.48

open browser at 

http://localhost:8080/
login = admin@opencti.io
pwd = <password>


`$ docker ps`
```
CONTAINER ID        IMAGE                                                 COMMAND                  CREATED             STATUS                    PORTS                                                 NAMES
fe47c2e95e8e        opencti/worker:3.3.2                                  "/entrypoint.sh"         23 minutes ago      Up 22 minutes                                                                   docker_worker_1
027b9a23014b        opencti/platform:3.3.2                                "/entrypoint.sh"         23 minutes ago      Up 23 minutes             0.0.0.0:8080->8080/tcp                                docker_opencti_1
f5fefaf16d21        opencti/connector-mitre:3.3.2                         "/entrypoint.sh"         23 minutes ago      Up 22 minutes                                                                   docker_connector-mitre_1
f9cc458b54a1        rabbitmq:3.8-management                               "docker-entrypoint.s…"   23 minutes ago      Up 23 minutes             4369/tcp, 5671-5672/tcp, 15671-15672/tcp, 25672/tcp   docker_rabbitmq_1
5d726c2e391e        opencti/connector-import-file-pdf-observables:3.3.2   "/entrypoint.sh"         23 minutes ago      Up 22 minutes                                                                   docker_connector-import-file-pdf-observables_1
a0d729d8633b        opencti/connector-opencti:3.3.2                       "/entrypoint.sh"         23 minutes ago      Up 22 minutes                                                                   docker_connector-opencti_1
511916f37840        opencti/connector-export-file-csv:3.3.2               "/entrypoint.sh"         23 minutes ago      Up 22 minutes                                                                   docker_connector-export-file-csv_1
5a7cdd52a24d        minio/minio:RELEASE.2020-05-16T01-33-21Z              "/usr/bin/docker-ent…"   23 minutes ago      Up 23 minutes (healthy)   0.0.0.0:9000->9000/tcp                                docker_minio_1
a4593c54538e        redis:6.0.5                                           "docker-entrypoint.s…"   23 minutes ago      Up 23 minutes             6379/tcp                                              docker_redis_1
0f39b9d1959d        graknlabs/grakn:1.7.2                                 "./grakn-docker.sh"      23 minutes ago      Up 23 minutes             0.0.0.0:48555->48555/tcp                              docker_grakn_1
df73bb3b5c51        docker.elastic.co/elasticsearch/elasticsearch:7.8.0   "/tini -- /usr/local…"   23 minutes ago      Up 23 minutes             9200/tcp, 9300/tcp                                    docker_elasticsearch_1
ec63f8b1e883        opencti/connector-export-file-stix:3.3.2              "/entrypoint.sh"         23 minutes ago      Up 22 minutes                                                                   docker_connector-export-file-stix_1
75896ed5ab08        opencti/connector-import-file-stix:3.3.2              "/entrypoint.sh"         23 minutes ago      Up 22 minutes                                                                   docker_connector-import-file-stix_1
```

### Stop OpenCTI docker

```
$ cd ~/openCTI/docker

$ docker-compose down
Stopping docker_worker_1                                ... done
Stopping docker_opencti_1                               ... done
Stopping docker_connector-mitre_1                       ... done
Stopping docker_rabbitmq_1                              ... done
Stopping docker_connector-import-file-pdf-observables_1 ... done
Stopping docker_connector-opencti_1                     ... done
Stopping docker_connector-export-file-csv_1             ... done
Stopping docker_minio_1                                 ... done
Stopping docker_redis_1                                 ... done
Stopping docker_grakn_1                                 ... done
Stopping docker_elasticsearch_1                         ... done
Stopping docker_connector-export-file-stix_1            ... done
Stopping docker_connector-import-file-stix_1            ... done



# Manual Setup
https://www.notion.so/Manual-deployment-b911beba44234f179841582ab3894bb1



# Utility

## UUID generator
https://www.uuidgenerator.net/version4



