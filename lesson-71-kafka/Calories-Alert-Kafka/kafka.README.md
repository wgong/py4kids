## Getting started with Apache Kafka in Python
https://towardsdatascience.com/getting-started-with-apache-kafka-in-python-604b3250aa05


Kafka relies on Zookeeper
https://linuxconfig.org/how-to-install-and-configure-zookeeper-in-ubuntu-18-04

The name space provided by Zookeeper is much like that of a standard file system

ZOOKEEPER & KAFKA INSTALL
https://www.bogotobogo.com/Hadoop/BigData_hadoop_Zookeeper_Kafka.php

ZOOKEEPER & KAFKA INSTALL : A SINGLE NODE AND A SINGLE BROKER CLUSTER - 2016
https://www.bogotobogo.com/Hadoop/BigData_hadoop_Zookeeper_Kafka_single_node_single_broker_cluster.php


$ sudo apt install openjdk-8-jdk
$ sudo useradd -m kafka     # create user=kafka
$ sudo adduser kafka sudo   # add user=kafka to sudo group
$ sudo apt-get install zookeeperd
Setting up zookeeperd (3.4.10-3) 
adduser: Warning: The home directory `/var/lib/zookeeper' does not belong to the user you are currently creating.

$ sudo netstat -nlpt | grep ':2181'
$ sudo netstat -nlpt | grep ':9092'

$ sudo service zookeeper stop

$ tar xvzf kafka_2.10-0.10.2.0.tgz --strip 1

>> start zookeeper
$ ~/kafka/bin/zookeeper-server-start.sh ~/kafka/config/zookeeper.properties  

>>>> How to stop zookeeper listening on port 2181
$ sudo netstat -pna | grep 2181
https://til.hashrocket.com/posts/e4c8c665a8-find-and-kill-all-processes-listening-on-a-port
$ lsof -n | grep LISTEN
$ lsof -n -i4TCP:[PORT] | grep LISTEN
$ lsof -n -i4TCP:[PORT] | grep LISTEN | awk '{ print $2 }' | xargs kill

$ sudo netstat -ntlp | grep :2181
tcp6       0      0 :::2181                 :::*                    LISTEN      2004/java           

$ sudo kill -TERM 2004  (2004 is PID for above issue)

# tutorial: http://blog.adnansiddiqi.me/getting-started-with-apache-kafka-in-python/

## use kafka/zookeeper

>> check if port 2181 in use
$ sudo netstat -ntlp | grep :2181
$ sudo kill -TERM 2058

>> start zookeeper
$ ~/kafka/bin/zookeeper-server-start.sh ~/kafka/config/zookeeper.properties  

>> start kafka
$ ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties

>> check status
$ jps
730 Kafka
1882 Jps
381 QuorumPeerMain

>> stop kafka
$ ~/kafka/bin/kafka-server-stop.sh ~/kafka/config/server.properties

>> stop zookeeper
$ ~/kafka/bin/zookeeper-server-stop.sh ~/kafka/config/zookeeper.properties   


>> create topic
$ ~/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1  --partitions 1 --topic Hello-Kafka


>> check topic
$ ls /tmp/kafka-logs

>> list topic
$ ~/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181

>> start producer
$ ~/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic Hello-Kafka
>hello kafka
>first greeting
>2nd greeting

>> check data-log
$ ~/kafka/bin/kafka-run-class.sh kafka.tools.DumpLogSegments --deep-iteration --print-data-log --files /tmp/kafka-logs/Hello-Kafka-0/00000000000000000000.log
Dumping /tmp/kafka-logs/test-0/00000000000000000000.log

Starting offset: 0
offset: 0 position: 0 CreateTime: 1573350001011 isvalid: true keysize: -1 valuesize: 15 magic: 2 compresscodec: NONE producerId: -1 producerEpoch: -1 sequence: -1 isTransactional: false headerKeys: [] payload: use kafka again
offset: 1 position: 83 CreateTime: 1573350009279 isvalid: true keysize: -1 valuesize: 29 magic: 2 compresscodec: NONE producerId: -1 producerEpoch: -1 sequence: -1 isTransactional: false headerKeys: [] payload: together with spark streaming
offset: 2 position: 180 CreateTime: 1573350022454 isvalid: true keysize: -1 valuesize: 29 magic: 2 compresscodec: NONE producerId: -1 producerEpoch: -1 sequence: -1 isTransactional: false headerKeys: [] payload: test Structured Streaming API

>> start consumer
$ ~/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic Hello-Kafka --from-beginning

type a few text msgs in producer terminal, 
you will see those msgs arrive in consumer terminal


>> install kafka-python
$ pip install kafka-python

>> Calories-Alert-Kafka
https://github.com/kadnan/Calories-Alert-Kafka

$ python producer-raw-recipies.py
$ python producer_consumer_parse_recipes.py
$ python consumer-notification.py

>> Kafka tool
http://www.kafkatool.com/features.html

>> install
$ sudo sh kafkatool.sh
/opt/kafkatool2

>> run
$ kafkatool


$ sudo apt autoremove  # remove unrequired pkgs


## Build a Distributed Streaming System with Apache Kafka and Python
https://scotch.io/tutorials/build-a-distributed-streaming-system-with-apache-kafka-and-python

https://github.com/amwaleh/Simple-stream-Kafka

see /home/gong/kafka/tutorials/Simple-stream-Kafka/README.md

## Kafka Python Tutorial for Fast Data Architecture

https://dzone.com/articles/kafka-python-tutorial-for-fast-data-architecture
