#!/bin/sh
sudo apt-get install mongodb python-setuptools libxslt1-dev libxslt1.1 libxml2-dev build-essential python-dev
sudo apt-get install git
sudo easy_install pip
sudo pip install -r install/requirements.txt
if [ "$1" = "optional" ]
then
	sudo pip install -r install/optional.txt
fi
