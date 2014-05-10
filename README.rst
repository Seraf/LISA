
About
#####

This project is like the J.A.R.V.I.S IA developed by Tony Stark in Iron Man.

I decided to create my own Digital Life Assistant because I didn't found any good project to contribute, or the concept wasn't good enough to fit my needs. I want something fast, easy to understand, easy to edit, easy to add features. Something small enough to run on a cheap computer like Raspberry Pi.

L.I.S.A will assist me like a Digital Like Assistant. It will give me usefull informations even if I didn't ask these, and answer me when I will ask something I want to know or to do. I actually have my house managed by a Vera-Lite controller (Zwave). L.I.S.A will be able to manage it (and other box with a simple module) and allow me to control with my house by voice.

State of the project : 

.. image:: https://travis-ci.org/Seraf/LISA.png?branch=master
    :target: https://travis-ci.org/Seraf/LISA

.. image:: https://coveralls.io/repos/Seraf/LISA/badge.png?branch=master
    :target: https://coveralls.io/r/Seraf/LISA?branch=master

.. image:: https://badge.waffle.io/seraf/lisa.png?label=ready&title=Ready 
    :target: https://waffle.io/seraf/lisa
    :alt: 'Stories in Ready'

.. image:: https://pypip.in/v/lisa-server/badge.png
    :target: https://pypi.python.org/pypi/lisa-server


Documentation
#############

You will find all documentation needed on https://lisa-project.readthedocs.org/en/latest/index.html

Overview
########

The architecture of L.I.S.A will be like this :

.. image:: docs/images/lisa-schema.png

The goal is to have the possibility to separate each element and let them communicate by network.
With this system you will be able to have one IA, multiple speech engine, and multiple clients.

Using twisted, the client should be able to transmit the data of the microphone but also the zone where the sound come from.
So the program will be able to answer in the zone where the sound was recorded.

LISA Engine
===========
.. include:: INSTALL.rst
