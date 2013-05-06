#!/bin/sh
git submodule update --init
sudo apt-get install mongodb
pip -r install Install/requirements.txt
