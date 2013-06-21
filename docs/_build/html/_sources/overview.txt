.. _overview:

#######
Overview
#######

The architecture of L.I.S.A will be like this :

.. image:: images/lisa-schema.png

The goal is to have the possibility to separate each element and let them communicate by network.
With this system you will be able to have one IA, multiple speech engine, and multiple clients.

Using twisted, the client should be able to transmit the data of the microphone but also the zone where the sound come from.
So the program will be able to answer in the zone where the sound was recorded.
