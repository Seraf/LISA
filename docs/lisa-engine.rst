.. _lisa-engine:

LISA Engine
=============

.. include:: ../LISA-Engine/README.rst
.. include:: ../LISA-Engine/INSTALL.rst

Configuration
-------------
LISA Engine come by default with some parameters contained in Configuration/lisa.json.

Here are the parameters available :

**lang**: The lang parameter will define which language to use in plugins. Some plugins will not be available in some
languages.

**lisa_url**: Is used in the lisa web part. Set here the dns you want to use.

**lisa_engine_port**: This field contains the port number (integer) where LISA will listen. You can choose any port
you want, take care to report the modification on clients too. By default, LISA will listen on the port 10042.

**lisa_web_port**: It is the port number (integer) where the webserver will listen. By default, LISA will listen on
the port 8000 to avoid conflict with any webserver already installed. If there is no one, it can be set to 80.

**Database**:

**server**: DNS or IP of where the mongodb server is located. By default it will use localhost.

**port**: Port used by mongodb (27017 by default).

**user**: User granted to connect to the lisa database ('lisa' by default).

**pass**: Pass of the user granted to connect the lisa database ('lisapowered' by default).

**debug**: Display the debug/verbose mode. The value is false by default.

Rules
-----
LISA Engine include a rule engine to allow the user to modify the behavior of a plugin.
The user can fill python code with condition which will be executed if conditions are matching.

For example, the output of a plugin can be overwritten depending the time of the day, or depending something else.
With this system and choosing carefully the rules order, you can chain plugins.

API
----
LISA embed an API for every possible actions on the website.
