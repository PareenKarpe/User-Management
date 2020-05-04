#!/bin/bash
sudo apt install python3-pip -y
sudo -H pip3 install virtualenv
mkdir pyrest
virtualenv pyrest
cd pyrest
source bin/activate
cd ..
sudo pip3 install flask
sudo pip3 install pylint
sudo pip3 install pyrest
sudo pip3 install pytest-html
sudo pip3 install bcrypt
sudo pip3 install boto3
sudo pip3 install ec2_metadata
sudo pip3 install mysql-connector-python
sudo pip3 install python-magic
sudo pip3 install werkzeug
sudo pip3 install pytest-html
echo "newstop"
