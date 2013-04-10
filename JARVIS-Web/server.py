import sys
import os

from twisted.application import internet, service
from twisted.web import server, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from sys import stdout
import twresource

class JarvisClient(Protocol):
    def sendMessage(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        stdout.write(data)

class JarvisClientFactory(ReconnectingClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected to Jarvis.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        return JarvisClient()

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

PORT = 8000

# Environment setup for your Django project files:
sys.path.append("jarvis")
os.environ['DJANGO_SETTINGS_MODULE'] = 'jarvis.settings'
from django.core.handlers.wsgi import WSGIHandler

def wsgi_resource():
    pool = threadpool.ThreadPool()
    pool.start()
    # Allow Ctrl-C to get you out cleanly:
    reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
    wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())
    return wsgi_resource


# Twisted Application Framework setup:
application = service.Application('twisted-django')

# WSGI container for Django, combine it with twisted.web.Resource:
# XXX this is the only 'ugly' part: see the 'getChild' method in twresource.Root 
wsgi_root = wsgi_resource()
root = twresource.Root(wsgi_root)

# Servce Django media files off of /media:
staticrsrc = static.File(os.path.join(os.path.abspath("."), "jarvis/static"))
root.putChild("static", staticrsrc)


jarvisclientfactory = JarvisClientFactory()
jarvisclient = reactor.connectTCP("localhost", 10042, jarvisclientfactory)

# The cool part! Add in pure Twisted Web Resouce in the mix
# This 'pure twisted' code could be using twisted's XMPP functionality, etc:
root.putChild("jarvis-engine", twresource.GoogleResource(jarvisclientfactory))

# Serve it up:
main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(application)
