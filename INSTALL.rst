Install
-------
The easiest way is to run the installer. As it's open source, you can see it will only install python packages necessary to run L.I.S.A.
You need to be in the top directory (LISA) where there is the README.md file.
::

  sh install/install.sh

Then, go into LISA-ENGINE and run :
::

  twistd -ny lisa.py

You should now create your first user :
::

  cd lisa
  python manage.py createsuperuser

.. warning:: As a new interface is in development, it will quickly change. The interface will use the API

To install plugins : http://localhost:8000/ (you should login first)(the interface have not Ajax yet, so after clicking on an action, reload the page with F5 !)
Plugins aren't translated yet. By default it will use the english language. Change the LISA-Engine/Configuration/lisa.json lang attribute to "en" to use english in plugins, then look how a plugin is built, you will see it's very easy to add a new language to the plugin.


You should be able to go to http://localhost:8000/speech/ (a webinterface will come soon and the twisted program will be daemonized as a service in the future).

