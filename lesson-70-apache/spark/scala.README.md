## How to install sbt on Ubuntu For Scala and Java projects
https://www.techrepublic.com/article/how-to-install-sbt-on-ubuntu-for-scala-and-java-projects/

```
sudo apt-get update
sudo apt-get upgrade -y

# install jdk
sudo apt-get install default-jdk -y

# get scala pkg
wget www.scala-lang.org/files/archive/scala-2.13.3.deb

# install scala
sudo dpkg -i scala-2.13.3.deb 
## test install
scala

# install sbt - scala build tool
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823

sudo apt-get update
sudo apt-get install sbt -y
## test install
sbt test

```