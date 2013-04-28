# -*- coding: UTF-8 -*-
import os,fnmatch,libs,json,sys,uuid
from twisted.internet.protocol import Factory, Protocol, ReconnectingClientFactory
from twisted.internet import reactor
from twisted.application import internet, service
from twisted.web import server, wsgi, static, resource
from twisted.python import threadpool
from django.core.handlers.wsgi import WSGIHandler
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.resource import WebSocketResource
from apscheduler.scheduler import Scheduler

scheduler = Scheduler()
scheduler.start()
configuration = json.load(open('Configuration/jarvis.json'))

class Jarvis(Protocol):
    def __init__(self,factory, bot_library):
        self.factory = factory
        self.bot_library = bot_library
        self.scheduler = scheduler

    def connectionMade(self):
        self.client_uuid = str(uuid.uuid1())
        self.factory.clients.append({"object": self, "zone": "", "type": "", "uuid": self.client_uuid})

    def connectionLost(self, reason):
        print 'Lost connection.  Reason:', reason
        for client in self.factory.clients:
            if client['object'] == self:
                self.factory.clients.remove(client)

    def dataReceived(self, data):
        jsonData = json.loads(data)
        for client in self.factory.clients:
            if client['object'] == self and (not client['type'] or not client['zone']):
                client['type'],client['zone'] = jsonData['type'],jsonData['zone']
        answer = self.bot_library.respond_to(str(jsonData['body'].encode('utf-8')))
        try:
            jsonAnswer = json.loads(answer)
        except:
            jsonAnswer = json.loads(json.dumps({"plugin": "Chat","method": "Chat","body": answer}))
        self.transport.write(json.dumps({'plugin': jsonAnswer['plugin'],'method': jsonAnswer['method'],\
                                         'body': jsonAnswer['body'],'client_uuid': self.client_uuid,\
                                         'from': jsonData['from']}))

class JarvisFactory(Factory):
    def __init__(self):
        try:
            self.bot_library = libs.RiveScriptBot()
            print "Successfully loaded bot"
        except:
            print "Couldn't load bot"
        self.clients = []

        for root, dirnames, filenames in os.walk('Plugins'):
            for filename in fnmatch.filter(filenames, '*.rs'):
                if os.path.normpath('lang/'+configuration['lang']) in root or filename=='begin.rs':
                    self.bot_library.learn(root)

    def buildProtocol(self, addr):
        return Jarvis(self,self.bot_library)

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
        reactor.connectTCP(configuration['jarvis_url'], 10042, self.jarvisclientfactory)
        WebSocketServerProtocol.connectionMade(self)

    def onMessage(self, msg, binary):
        self.jarvisclientfactory.protocol.sendMessage(json.dumps( \
            {"from": "Jarvis-Web","type": "Chat", "body": unicode(msg.decode('utf-8')), "zone": "WebSocket"}))

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
# Twisted Application Framework setup:
application = service.Application('JARVIS')

# Environment setup for Django project files:
sys.path.append(os.path.join(os.path.abspath("."), "web"))
sys.path.append(os.path.join(os.path.abspath("."), "web/jarvis"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.jarvis.settings'
wsgi_root = wsgi_resource()
root = Root(wsgi_root)

staticrsrc = static.File(os.path.join(os.path.abspath("."), "web/jarvis/static"))
root.putChild("static", staticrsrc)

socketfactory = WebSocketServerFactory("ws://"+configuration['jarvis_url']+":8000", debug = False)
socketfactory.protocol = WebSocketProtocol
socketresource = WebSocketResource(socketfactory)
root.putChild("websocket", socketresource)

# Serve it up:
internet.TCPServer(8000, server.Site(root)).setServiceParent(application)
internet.TCPServer(10042, JarvisFactory()).setServiceParent(application)