===============
Troubleshooting
===============

The intent of the troubleshooting section is to introduce solutions to a
number of common issues encountered by users and the tools that are available
to aid debug the code.

.. toctree::
    :maxdepth: 2
    :glob:

    *

What Ports do the Server and Clients Need Open?
===============================================

No ports need to be opened up on clients. For the server, TCP ports 10042,
10043 and 8000 (or 80) need to be open. If you can't connect on you server,
and can't access the web interface, it could be a firewall problem.

You can check port connectivity with the nc command:

.. code-block:: bash

  nc -v -z lisa.server 10042
  nc -v -z lisa.server 8000
