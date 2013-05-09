#!/bin/sh
git submodule update --init
sudo apt-get install mongodb python-setuptools libxslt1-dev libxslt1.1 libxml2-dev build-essential python-dev
sudo easy_install pip
sudo pip install -r install/requirements.txt
