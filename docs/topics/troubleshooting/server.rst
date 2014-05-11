======================
Server Troubleshooting
======================

If your server is having issues such as server not returning data, slow
execution times, or a variety of other issues the
:doc:`Server troubleshooting page
</topics/troubleshooting/server>` contains details on troubleshooting the most
common issues encountered.


Running in the Foreground
=========================

A great deal of information is available via the debug logging system, if you
are having issues is to run the server in the foreground to display logs in
the console:

.. code-block:: bash

  twistd -n lisa-server
