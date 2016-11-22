#!/bin/sh

#for getting everything ready to go on the EC2s I'm using for scraping

sudo apt-get update  # To get the latest package lists
sudo apt-get install python -y
sudo apt install python-pip -y


#go mongo go
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections
sudo mkdir /data
cd /data
sudo mkdir db


sudo pip install pymongo
sudo pip install pandas
sudo pip install numpy
sudo pip install bs4
sudo pip install requests
# sudo pip install sklearn
# sudo pip install matplotlib
# sudo pip install seaborn
# sudo pip install ipython
# pip install gensim
