Frequently Asked Questions
==========================

.. contents:: FAQ

Is LISA open-source ?
---------------------

Yes. LISA is 100% open-source, including all APIs.

Is LISA full local mode or does it need an Internet connection ?
----------------------------------------------------------------

LISA is actually needing an Internet connection. I work on it to have something fully working even if your
connection is broken.

LISA need internet at least for his client (because speech recognition is online) and to use Wit Engine
on the server side. Wit is also working on a local server for Wit. Once it will be available, it will be
backported in LISA as soon as possible.

Why LISA use mongodb as database ?
----------------------------------

I am a DevOps, then when I code, I always think about how will it work in production. Is it scalable ?
Mongodb let LISA to scale and support loss of a server. The database can be distribued accross your
clients for example. The NoSQL technology allow developers to build plugins easily.

As plugins and configuration are stored in the mongodb database, you can scale the LISA server with
a load balancer.

The only problem is a lack of support for ARM. But there's a ticket opened on their JIRA issue tracker.

What ports should I open on my firewall ?
-----------------------------------------

LISA use by default the port 10042 to communicate between client and server, and port 8000 for the webserver.