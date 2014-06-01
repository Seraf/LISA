===========================
Create a plugin for L.I.S.A
===========================

Creating a plugin is very easy, thanks to the cli tool.

To create your plugin, type (in the virtualenv):

.. code-block:: console

    lisa-cli plugin PLUGINNAME --create

Then, answer the questions, and you will find the plugin in your virtualenv.

.. code-block:: console

    /home/alivelisa/.virtualenvs/lisa/local/lib/python2.7/site-packages/lisa/plugins/PLUGINNAME

By creating a new plugin you don't install it automatically. So write the code you want in the plugin, then install it
in order to use the plugin. Don't forget to install it in dev mode (by using --dev)

.. seealso::

    :doc:`Distribute your Plugin </topics/plugins/distribute>`
