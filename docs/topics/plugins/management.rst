=================
Plugin Management
=================

The plugin management is usefull to quickly manage plugins from Command Line Interface.
It uses the same function than the web interface so it has the same behavior.

To list the functionnalities

.. code-block:: console

    $ lisa-cli plugin --help
    Usage: /home/alivelisa/.virtualenvs/lisa/bin/lisa-cli plugin [options] <plugin_name>

    Manage the plugins

    Options:
      --list                List all plugins and show their status
      --create              Create a template plugin with a given name
      --enable              Enable a plugin
      --disable             Disable a plugin
      --install             Install a plugin
      --dev                 Dev mode
      --uninstall           Uninstall a plugin
      --upgrade             Upgrade a plugin
      -h, --help            show this help message and exit

:list: This option does not need to be called with a plugin name.

.. code-block:: console

    $ lisa-cli plugin --list
    ChatterBot => [Installed] [Enabled]
    BBox => [Installed] [Enabled]
    ProgrammeTV => [Installed] [Enabled]
    Cinema => [Not installed] [Not enabled]
    Meteo => [Not installed] [Not enabled]
    SNCF => [Not installed] [Not enabled]
    Shopping => [Not installed] [Not enabled]
    Wifiledlamps => [Not installed] [Not enabled]


:create: This option will create a plugin in your plugins directory. It will ask some questions to auto-configure the plugin.

.. code-block:: console

    $ lisa-cli plugin --create PLUGINNAME
    What is your full name ? : Lisa
    What is your email ? : lisa@lisa-project.net
    [OK] Plugin created


:enable / disable: This option will enable or disable a plugin. That means the plugin the plugin still exists in database and on filesystem but will not be loaded by the plugin manager.

.. code-block:: console

    $ lisa-cli plugin --enable PLUGINNAME
    [OK] Plugin enabled

.. code-block:: console

    $ lisa-cli plugin --disable PLUGINNAME
    [OK] Plugin disabled

:dev: This option allow you to specify that you are writing a plugin. It will not download it on Python Package Index but use the local plugin instead. It will not do anything on the filesystem but only on database. It is mainly used for install and uninstall function. When used with install, it will update all fields in database according your local plugin files. If you use uninstall with the dev mode, it will not delete the json file, only records in the database.

:install: This option will install a plugin. By default it download the package from Python Package Index then read the json file and install all components (rules, crons, intents, plugin configuration) in the database.

.. code-block:: console

    $ lisa-cli plugin --install PLUGINNAME
    [OK] Plugin installed

:uninstall: This option will uninstall a plugin. By default it will remove the package and all the files related to the plugin and remove entries related to the plugin in database.

.. code-block:: console

    $ lisa-cli plugin --uninstall PLUGINNAME
    [OK] Plugin uninstalled

:upgrade: This option is not implemented yet.

.. code-block:: console

    $ lisa-cli plugin --upgrade PLUGINNAME
    [OK] Plugin upgraded
