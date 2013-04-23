JARVIS Speech
======
This directory contains the program who receive the stream for JARVIS-Client, analyze it with pocketsphinx and
send the result to the JARVIS-Engine

apt-get install build-essential bison python-dev
tar -zxvf sphinxbase-0.8.tar.gz
./configure
make
sudo make install
tar -zxvf pocketsphinx-0.8.tar.gz
./configure
make
sudo make install

http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/French%20Language%20Model/
http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/French%20F2%20Telephone%20Acoustic%20Model/
-> JARVIS-Speech/libs/