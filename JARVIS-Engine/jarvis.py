# -*- coding: UTF-8 -*-
import os,libs,json,sys,uuid
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.application import internet, service
from twisted.web import server, wsgi, static, resource
from twisted.python import threadpool, log
from django.core.handlers.wsgi import WSGIHandler
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.resource import WebSocketResource
from pymongo import MongoClient
from libs.txscheduler.manager import ScheduledTaskManager
from libs.txscheduler.service import ScheduledTaskService

configuration = json.load(open('Configuration/jarvis.json'))
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
if not os.path.exists(dir_path + '/' + 'Plugins'):
    os.mkdir(dir_path + '/' + 'Plugins')

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

    def connectionMade(self):
        self.client_uuid = str(uuid.uuid1())
        self.factory.clients.append({"object": self, "zone": "", "type": "", "uuid": self.client_uuid})

    def connectionLost(self, reason):
        log.msg('Lost connection.  Reason:', reason)
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
            log.msg("Successfully loaded bot")
        except:
            log.msg("Couldn't load bot")
        self.clients = []
        self.syspath = sys.path
        mongo = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = mongo.jarvis

        # Install the default Chatterbot plugin
        self.build_grammar()

    def build_grammar(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        # Load enabled plugins for the main language
        for plugin in self.database.plugins.find( { "enabled": True, "lang": configuration['lang'] } ):
            sys.path.append(str(os.path.normpath(dir_path + '/Plugins/' + plugin['name'] + '/lang/' \
                                             + configuration['lang'] + '/modules/')))
            self.bot_library.learn(os.path.normpath('Plugins/' + plugin['name'] + '/lang/' \
                                                    + configuration['lang'] + '/text'))

    def buildProtocol(self, addr):
        self.Jarvis = Jarvis(self,self.bot_library)
        return self.Jarvis

class Root(resource.Resource):
    def __init__(self, wsgi_resource):
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
        reactor.connectTCP(configuration['jarvis_url'], configuration['jarvis_engine_port'], self.jarvisclientfactory)

    def onMessage(self, msg, binary):
        self.jarvisclientfactory.protocol.sendMessage(json.dumps( \
            {"from": "Jarvis-Web","type": "Chat", "body": unicode(msg.decode('utf-8')), "zone": "WebSocket"}))

class JarvisReload(resource.Resource):
    def __init__(self, JarvisFactory):
        self.JarvisFactory = JarvisFactory
        sys.path = self.JarvisFactory.syspath
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        self.JarvisFactory.build_grammar()
        return "OK"

    def render_GET(self, request):
        self.JarvisFactory.build_grammar()
        return "OK"

# Twisted Application Framework setup:
application = service.Application('JARVIS')

# Instance of JarvisFactory to pass it to other services
JarvisFactory = JarvisFactory()
# Create a task manager to pass it to other services
taskman = ScheduledTaskManager(configuration)
scheduler = ScheduledTaskService(taskman)

# Environment setup for Django project files:
sys.path.append(os.path.join(os.path.abspath("."), "web"))
sys.path.append(os.path.join(os.path.abspath("."), "web/jarvis"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.jarvis.settings'

# Creating MultiService
multi = service.MultiService()
pool = threadpool.ThreadPool()
tps = ThreadPoolService(pool)
tps.setServiceParent(multi)
resource_wsgi = wsgi.WSGIResource(reactor, tps.pool, WSGIHandler())
root = Root(resource_wsgi)

staticrsrc = static.File(os.path.join(os.path.abspath("."), "web/jarvis/static"))
root.putChild("static", staticrsrc)
root.putChild("reload", JarvisReload(JarvisFactory))

socketfactory = WebSocketServerFactory("ws://" + configuration['jarvis_url'] + ":" +\
                                       str(configuration['jarvis_web_port']),debug=False)
socketfactory.protocol = WebSocketProtocol
socketresource = WebSocketResource(socketfactory)
root.putChild("websocket", socketresource)


# Serve it up:
internet.TCPServer(configuration['jarvis_web_port'], server.Site(root)).setServiceParent(multi)
internet.TCPServer(configuration['jarvis_engine_port'], JarvisFactory).setServiceParent(multi)
scheduler.setServiceParent(multi)
multi.setServiceParent(application)
