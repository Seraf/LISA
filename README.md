JARVIS
======

Repository of a JARVIS system to control my house
![Image](docs/images/jarvis-architecture.png?raw=true)

Example :
apt-get install julius julius-voxforge

Launch with:
julius -input adinnet -48 -realtime -v sample.dict  -dfa sample.dfa -h /usr/share/julius-voxforge/acoustic/hmmdefs -hlist /usr/share/julius-voxforge/acoustic/tiedlist
