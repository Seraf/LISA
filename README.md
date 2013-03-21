JARVIS
======

Repository of a JARVIS system to control my house
![Image](docs/images/jarvis-architecture.png?raw=true)

Complete redesign of the application using cmusphinx:  
The goal is to have the possibility to separate each element and let them communicate by network.
With this system you will be able to have one IA, multiple speech engine, and multiple clients.

Using twisted, the client should be able to transmit the data of the microphone but also the zone where the sound come from.
So the program will be able to answer in the zone where the sound was recorded.

USEFULL RESSOURCE TO CHECK FOR FRENCH LANGUAGE : http://www-lium.univ-lemans.fr/fr/content/ressources
