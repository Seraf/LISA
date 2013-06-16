About
#####

This project is one of the lot of J.A.R.V.I.S project we can found on the net. (J.A.R.V.I.S is the IA developed by Tony Stark in Iron Man)

I decided to create my own version because I didn't found any good project to contribute. Or the concept wasn't good enough to fit my needs. I want something fast, easy to understand, easy to edit, easy to add features. Something small enough to run on a cheap computer like Raspberry Pi.

J.A.R.V.I.S will assist me like a Digital Like Assistant. It will give me usefull informations even if I didn't ask these, and answer me when I will ask something I want to know or to do. I actually have my house managed by a Vera-Lite controller (Zwave). J.A.R.V.I.S will be able to manage it (and other box with a simple module) and allow me to control with my house by voice.

Documentation
#############
You will find all documentation needed on https://jarvis-system.readthedocs.org/en/latest/index.html

Overview
#######

The architecture of J.A.R.V.I.S will be like this :

.. image:: docs/images/jarvis-schema.png

The goal is to have the possibility to separate each element and let them communicate by network.
With this system you will be able to have one IA, multiple speech engine, and multiple clients.

Using twisted, the client should be able to transmit the data of the microphone but also the zone where the sound come from.
So the program will be able to answer in the zone where the sound was recorded.

JARVIS Engine
=============

.. include:: ../JARVIS-Engine/README.rst
.. include:: ../JARVIS-Engine/INSTALL.rst
