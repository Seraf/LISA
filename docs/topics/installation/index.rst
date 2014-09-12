.. _installation:

============
Installation
============
.. seealso::

    :doc:`Contributing to L.I.S.A </topics/development/contributing>`

Quick Install
-------------
.. code-block:: bash

    # Installing Debian dependencies
    sudo apt-get install mongodb python-setuptools libxslt1-dev libxslt1.1 libxml2-dev libffi-dev build-essential python-dev libssl-dev python-openssl libyaml-dev
    # Installing pip
    sudo easy_install pip
    # Installing tools to create a python virtual environment
    sudo pip install virtualenv virtualenvwrapper
    # Create the lisa user (you can choose another username)
    sudo useradd -s /bin/bash -m alivelisa
    # Login with this user
    sudo su - alivelisa
    # Set environment variable to use correctly the new virtual environment
    export WORKON_HOME=$HOME/.virtualenvs
    echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
    export PROJECT_HOME=$HOME/
    echo "export PROJECT_HOME=$HOME/" >> ~/.bashrc
    source /usr/local/bin/virtualenvwrapper.sh
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
    # Create the virtual environment named "lisa"
    mkproject lisa
    # This command let you enter your environment and load all libraries. Now Lisa is usable
    workon lisa
    # Install twisted then the LISA server
    pip install twisted
    pip install lisa-server
    # Create your user
    lisa-cli createsuperuser


Platform-specific Installation Instructions
-------------------------------------------

These guides go into detail how to install L.I.S.A on a given platform.

.. toctree::
    :maxdepth: 1

    arch
    debian
    fedora
    freebsd
    gentoo
    osx
    rhel
    solaris
    synology
    windows
    suse


Dependencies
------------

L.I.S.A should run on any Unix-like platform so long as the dependencies are met.

.. code-block:: none

    mongoengine >= 0.8.7
    Django >= 1.6.2
    Sphinx >= 1.2.2
    Twisted >= 13.2.0
    autobahn >= 0.8.7
    pymongo >= 2.7
    requests >= 2.2.1
    django-tastypie >= 0.11.0
    django-tastypie-mongoengine >= 0.4.5
    django-tastypie-swagger >= 0.1.2
    pytz >= 2014.2
    pyOpenSSL == 0.13
    lisa-plugin-ChatterBot
    PyWit >= 0.2.0


Upgrading L.I.S.A
-----------------

To upgrade L.I.S.A manually, you can upgrade the python package (in the virtualenv):

.. code-block:: console

    pip install --upgrade lisa-server
