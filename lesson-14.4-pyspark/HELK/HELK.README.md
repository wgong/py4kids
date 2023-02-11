
### Documentations

- https://thehelk.com/installation.html
- https://medium.com/threat-hunters-forge/threat-hunting-with-etw-events-and-helk-part-1-installing-silketw-6eb74815e4a0

- https://cyberwardog.blogspot.com/

- https://cyberwardog.blogspot.com/2018/04/welcome-to-helk-enabling-advanced_9.html

- https://stackoverflow.com/questions/38830610/access-jupyter-notebook-running-on-docker-container
- https://medium.com/threat-hunters-forge/writing-an-interactive-book-over-the-threat-hunter-playbook-with-the-help-of-the-jupyter-book-3ff37a3123c7




### Install

#### remove docker
sudo systemctl status docker

sudo systemctl stop docker

** after uninstall docker, needs to reboot 




#### install HELK docker containers

~/projects/HELK/docker$ sudo ./helk_install.sh

$ tail -f /var/log/helk-install.log  # monitor install progress


4. KAFKA + KSQL + ELK + NGINX + SPARK + JUPYTER + ELASTALERT

Set HELK IP. Default value is your current IP: 192.168.0.114

Set HELK Kibana UI Password: helkguy  (Default user is helk)


ERROR:

Creating helk-elasticsearch ... done
Creating helk-kibana        ... done
Creating helk-nginx         ... 
Creating helk-nginx         ... error
Host is already in use by another container

ERROR: for helk-nginx  Cannot start service helk-nginx: driver failed programming external connectivity on endpoint helk-nginx (73a6dbb038e455984438a79a9322d839b32a8f89bb79b373266dCreating helk-logstash      ... done
Creating helk-zookeeper     ... done
Creating helk-spark-master  ... done
Creating helk-elastalert    ... done
Creating helk-jupyter       ... done
Creating helk-kafka-broker  ... done
Creating helk-spark-worker  ... done
Creating helk-ksql-server   ... done
Creating helk-ksql-cli      ... done

ERROR: for helk-nginx  Cannot start service helk-nginx: driver failed programming external connectivity on endpoint helk-nginx (73a6dbb038e455984438a79a9322d839b32a8f89bb79b373266d7471c19edbff): Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use
Encountered errors while bringing up the project.

http://localhost:80 is being used by Apache2

#### stop Apache2 service if running

$ sudo systemctl status|stop|start|restart apache2.service

#### manage HELK containers

You can stop all the HELK docker containers by running the following command:
$ sudo docker-compose -f helk-kibana-notebook-analysis-alert-basic.yml stop   # stop helk

Stopping helk-ksql-cli      ... done
Stopping helk-ksql-server   ... done
Stopping helk-spark-worker  ... done
Stopping helk-kafka-broker  ... done
Stopping helk-jupyter       ... done
Stopping helk-elastalert    ... done
Stopping helk-spark-master  ... done
Stopping helk-zookeeper     ... done
Stopping helk-logstash      ... done
Stopping helk-kibana        ... done
Stopping helk-elasticsearch ... done


#### start HELK

$ sudo docker-compose -f helk-kibana-notebook-analysis-alert-basic.yml start

Starting helk-elasticsearch ... done
Starting helk-kibana        ... done
Starting helk-logstash      ... done
Starting helk-nginx         ... done
Starting helk-zookeeper     ... done
Starting helk-kafka-broker  ... done
Starting helk-ksql-server   ... done
Starting helk-ksql-cli      ... done
Starting helk-jupyter       ... done
Starting helk-spark-master  ... done
Starting helk-spark-worker  ... done
Starting helk-elastalert    ... done

#### Check docker process status

$ sudo docker ps

CONTAINER ID   IMAGE                                                 COMMAND                  CREATED      STATUS              PORTS                                                                                                                                                                                                                                                                                                                                                           NAMES
5a5af6f41bb7   confluentinc/cp-ksql-cli:5.1.3                        "/bin/sh"                2 days ago   Up About a minute                                                                                                                                                                                                                                                                                                                                                                   helk-ksql-cli
accd0b2651a5   confluentinc/cp-ksql-server:5.1.3                     "/etc/confluent/dock…"   2 days ago   Up About a minute   0.0.0.0:8088->8088/tcp, :::8088->8088/tcp                                                                                                                                                                                                                                                                                                                       helk-ksql-server
2f54c92556d0   otrf/helk-spark-worker:2.4.5                          "./spark-worker-entr…"   2 days ago   Up About a minute                                                                                                                                                                                                                                                                                                                                                                   helk-spark-worker
79e62a0bbfe9   otrf/helk-kafka-broker:2.4.0                          "./kafka-entrypoint.…"   2 days ago   Up About a minute   0.0.0.0:9092->9092/tcp, :::9092->9092/tcp                                                                                                                                                                                                                                                                                                                       helk-kafka-broker
a44c7d719739   docker_helk-jupyter                                   "/opt/jupyter/script…"   2 days ago   Up About a minute   8000/tcp, 8888/tcp                                                                                                                                                                                                                                                                                                                                              helk-jupyter
77a074d219b6   otrf/helk-elastalert:latest                           "./elastalert-entryp…"   2 days ago   Up About a minute                                                                                                                                                                                                                                                                                                                                                                   helk-elastalert
8d9b8d8480a7   otrf/helk-spark-master:2.4.5                          "./spark-master-entr…"   2 days ago   Up About a minute   7077/tcp, 0.0.0.0:8080->8080/tcp, :::8080->8080/tcp                                                                                                                                                                                                                                                                                                             helk-spark-master
e2981002c372   otrf/helk-zookeeper:2.4.0                             "./zookeeper-entrypo…"   2 days ago   Up About a minute   2181/tcp, 2888/tcp, 3888/tcp                                                                                                                                                                                                                                                                                                                                    helk-zookeeper
860d7b94c6f7   otrf/helk-logstash:7.6.2.1                            "/usr/share/logstash…"   2 days ago   Up About a minute   0.0.0.0:3515->3515/tcp, :::3515->3515/tcp, 0.0.0.0:5044->5044/tcp, :::5044->5044/tcp, 0.0.0.0:5514->5514/tcp, 0.0.0.0:5514->5514/udp, :::5514->5514/tcp, :::5514->5514/udp, 0.0.0.0:8515-8516->8515-8516/tcp, :::8515-8516->8515-8516/tcp, 0.0.0.0:8531->8531/tcp, :::8531->8531/tcp, 0.0.0.0:8515-8516->8515-8516/udp, :::8515-8516->8515-8516/udp, 9600/tcp   helk-logstash
64b49f93c1ea   otrf/helk-nginx:0.3.0                                 "/opt/helk/scripts/n…"   2 days ago   Up About a minute   0.0.0.0:80->80/tcp, :::80->80/tcp, 0.0.0.0:443->443/tcp, :::443->443/tcp                                                                                                                                                                                                                                                                                        helk-nginx
a3e1f44bf01a   docker.elastic.co/kibana/kibana:7.6.2                 "/usr/share/kibana/s…"   2 days ago   Up About a minute   5601/tcp                                                                                                                                                                                                                                                                                                                                                        helk-kibana
554836b9ab27   docker.elastic.co/elasticsearch/elasticsearch:7.6.2   "/usr/share/elastics…"   2 days ago   Up About a minute   9200/tcp, 9300/tcp                                                                                                                                                                                                                                                                                                                                              helk-elasticsearch


#### Login to Kibana

https://0.0.0.0:443/
https://192.168.0.114/app/kibana#/home
helk/helkguy

#### KSQL
http://0.0.0.0:8088/info

#### Spark UI
http://0.0.0.0:8080/

#### Jupyter notebook


sudo docker exec -ti helk-jupyter bash  # log into container for helk-jupyter
jupyter-notebook list  # get token
http://0.0.0.0:8888/jupyter/?token=b661b31b065f9aa87ebb31ead1d8bed725f66d0d426cac84

HELK JUPYTER SERVER URL: https://${HOST_IP}/jupyter

Figuring this out by reading `helk_install.sh`
