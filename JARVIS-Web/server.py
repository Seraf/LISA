import sys
import os

from twisted.application import internet, service
from twisted.web import server, wsgi, static, resource
from twisted.python import threadpool
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from django.core.handlers.wsgi import WSGIHandler
from autobahn.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS
import json

class JarvisClient(Protocol):
    def __init__(self, WebSocketProtocol):
        self.WebSocketProtocol = WebSocketProtocol
    def sendMessage(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        self.WebSocketProtocol.sendMessage(data)

class JarvisClientFactory(ReconnectingClientFactory):
    def __init__(self, WebSocketProtocol):
        self.WebSocketProtocol = WebSocketProtocol
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        self.protocol = JarvisClient(self.WebSocketProtocol)
        print 'Connected to Jarvis.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

class WebSocketProtocol(WebSocketServerProtocol):
    def connectionMade(self):
        self.jarvisclientfactory = JarvisClientFactory(self)
        reactor.connectTCP("localhost", 10042, self.jarvisclientfactory)
        WebSocketServerProtocol.connectionMade(self)

    def onMessage(self, msg, binary):
        print "sending echo:", msg
        self.jarvisclientfactory.protocol.sendMessage(json.dumps( \
            {"from": "Jarvis-Web","type": "Chat", "body": unicode(msg)}))
        self.sendMessage(msg, binary)


class Root(resource.Resource):
    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource

def wsgi_resource():
    pool = threadpool.ThreadPool()
    pool.start()
    # Allow Ctrl-C to get you out cleanly:
    reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
    wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())
    return wsgi_resource

PORT = 8000

# Environment setup for your Django project files:
sys.path.append("jarvis")
os.environ['DJANGO_SETTINGS_MODULE'] = 'jarvis.settings'

# Twisted Application Framework setup:
application = service.Application('twisted-django')

# WSGI container for Django, combine it with twisted.web.Resource:
# XXX this is the only 'ugly' part: see the 'getChild' method in twresource.Root 
wsgi_root = wsgi_resource()
root = Root(wsgi_root)

# Servce Django media files off of /media:
staticrsrc = static.File(os.path.join(os.path.abspath("."), "jarvis/static"))
root.putChild("static", staticrsrc)

factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
factory.protocol = WebSocketProtocol
listenWS(factory)

# Serve it up:
main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(application)
