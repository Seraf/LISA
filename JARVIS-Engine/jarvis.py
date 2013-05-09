# -*- coding: UTF-8 -*-
import os,fnmatch,libs,json,sys,uuid
from twisted.internet.protocol import Factory, Protocol
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

class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()

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
        libs.RulesEngine(configuration).Rules(jsonData, jsonAnswer, self)


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

class Root(resource.Resource):
    def __init__(self, wsgi_resource):
        print wsgi_resource
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource

class WebSocketProtocol(WebSocketServerProtocol):
    def connectionMade(self):
        WebSocketServerProtocol.connectionMade(self)
        self.jarvisclientfactory = libs.JarvisClientFactory(self)
        reactor.connectTCP(configuration['jarvis_url'], configuration['jarvis_engine_port'], \
                           self.jarvisclientfactory)

    def onMessage(self, msg, binary):
        self.jarvisclientfactory.protocol.sendMessage(json.dumps( \
            {"from": "Jarvis-Web","type": "Chat", "body": unicode(msg.decode('utf-8')), "zone": "WebSocket"}))

# Twisted Application Framework setup:
application = service.Application('JARVIS')

# Environment setup for Django project files:
sys.path.append(os.path.join(os.path.abspath("."), "web"))
sys.path.append(os.path.join(os.path.abspath("."), "web/jarvis"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.jarvis.settings'

multi = service.MultiService()
pool = threadpool.ThreadPool()
tps = ThreadPoolService(pool)
tps.setServiceParent(multi)
resource_wsgi = wsgi.WSGIResource(reactor, tps.pool, WSGIHandler())
root = Root(resource_wsgi)

staticrsrc = static.File(os.path.join(os.path.abspath("."), "web/jarvis/static"))
root.putChild("static", staticrsrc)

socketfactory = WebSocketServerFactory("ws://" + configuration['jarvis_url'] + ":" +\
                                       str(configuration['jarvis_web_port']),debug=False)
socketfactory.protocol = WebSocketProtocol
socketresource = WebSocketResource(socketfactory)
root.putChild("websocket", socketresource)

# Serve it up:
internet.TCPServer(configuration['jarvis_web_port'], server.Site(root)).setServiceParent(multi)
internet.TCPServer(configuration['jarvis_engine_port'], JarvisFactory()).setServiceParent(multi)
multi.setServiceParent(application)
