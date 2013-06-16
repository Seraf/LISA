JARVIS
======

This project is one of the lot of J.A.R.V.I.S project we can found on the net.
(J.A.R.V.I.S is the IA developed by Tony Stark in Iron Man)

I decided to create my own version because I didn't found any good project to contribute. Or the concept wasn't good enough to fit my needs.
I want something fast, easy to understand, easy to edit, easy to add features. Something small enough to run on a cheap computer like Raspberry Pi.

J.A.R.V.I.S will assist me like a Digital Like Assistant. It will give me usefull informations even if I didn't ask these, and answer me when I will ask something I want to know or to do.
I actually have my house managed by a Vera-Lite controller (Zwave). J.A.R.V.I.S will be able to manage it (and other box with a simple module) and allow me to control with my house by voice.

The technologies I plan to use are :
* Python
* Twisted (Python Network Framework)
* Rivescript (Langage parsing)
* Pocketsphinx (speech to text)
* Mongodb (as database)

The architecture of J.A.R.V.I.S will be like this :
![Image](docs/images/jarvis-schema.png?raw=true)

The goal is to have the possibility to separate each element and let them communicate by network.
With this system you will be able to have one IA, multiple speech engine, and multiple clients.

Using twisted, the client should be able to transmit the data of the microphone but also the zone where the sound come from.
So the program will be able to answer in the zone where the sound was recorded.

INSTALL
======
The easiest way is to run the installer. As it's open source, you can see it will only install python packages necessary to run J.A.R.V.I.S.
You need to be in the top directory (JARVIS) where there is the README.md file.
<pre>
sh install/install.sh
</pre>
(Actually I use the django toolbar to debug ... so add it with:)
<pre>
sudo pip -r install/optional.txt
</pre>

Then, go into JARVIS-ENGINE and run :
<pre>
twistd -ny jarvis.py
</pre>
To install plugins : http://localhost:8000/plugins/ (the interface have not Ajax yet, so after clicking on an action, reload the page with F5 !)
Plugins aren't translated yet. By default it will use the english language. Change the JARVIS-Engine/Configuration/jarvis.json lang attribute to "en" to use english in plugins, then look how a plugin is built, you will see it's very easy to add a new language to the plugin.


You should be able to go to http://localhost:8000/speech/ (a webinterface will come soon and the twisted program will be daemonized as a service in the future).
