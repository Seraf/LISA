# -*- coding: UTF-8 -*-
import os,libs,json,sys,uuid
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor, ssl
from twisted.application import internet, service
from twisted.web import server, wsgi, static
from twisted.python import threadpool, log
from django.core.handlers.wsgi import WSGIHandler
from autobahn.websocket import WebSocketServerFactory
from autobahn.resource import WebSocketResource
from pymongo import MongoClient
from libs.txscheduler.manager import ScheduledTaskManager
from libs.txscheduler.service import ScheduledTaskService
from OpenSSL import SSL

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
configuration = json.load(open(os.path.normpath(dir_path + '/' + 'Configuration/lisa.json')))
if not os.path.exists(os.path.normpath(dir_path + '/' + 'Plugins')):
    os.mkdir(os.path.normpath(dir_path + '/' + 'Plugins'))

class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()

class ServerTLSContext(ssl.DefaultOpenSSLContextFactory):
    def __init__(self, *args, **kw):
        kw['sslmethod'] = SSL.TLSv1_METHOD
        ssl.DefaultOpenSSLContextFactory.__init__(self, *args, **kw)

class Lisa(Protocol):
    def __init__(self,factory, bot_library):
        self.factory = factory
        self.bot_library = bot_library

    def answertoclient(self, jsondata):
        self.transport.write(jsondata)

    def connectionMade(self):
        self.client_uuid = str(uuid.uuid1())
        self.factory.clients.append({"object": self, "zone": "", "type": "", "uuid": self.client_uuid})
        if configuration['enable_secure_mode']:
            ctx = ServerTLSContext(
                privateKeyFileName=os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.key'),
                certificateFileName= os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.crt')
            )
            self.transport.startTLS(ctx, self.factory)

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
        libs.RulesEngine(configuration).Rules(jsonData=jsonData, lisaprotocol=self)

class LisaFactory(Factory):
    def __init__(self):
        try:
            self.bot_library = libs.RiveScriptBot()
            log.msg("Successfully loaded bot")
        except:
            log.msg("Couldn't load bot")
        self.clients = []
        self.syspath = sys.path
        mongo = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = mongo.lisa
        self.build_grammar()

    def build_grammar(self):
        self.bot_library.learn(os.path.normpath(dir_path + '/' + 'Configuration/'))
        # Load enabled plugins for the main language
        for plugin in self.database.plugins.find( { "enabled": True, "lang": configuration['lang'] } ):
            sys.path.append(str(os.path.normpath(dir_path + '/Plugins/' + plugin['name'] + '/lang/' \
                                             + configuration['lang'] + '/modules/')))
            self.bot_library.learn(os.path.normpath(dir_path + '/' + 'Plugins/' + plugin['name'] + '/lang/' \
                                                    + configuration['lang'] + '/text'))

    def buildProtocol(self, addr):
        self.Lisa = Lisa(self,self.bot_library)
        return self.Lisa

    def LisaReload(self):
        log.msg("Reloading L.I.S.A Engine")
        sys.path = self.syspath
        self.build_grammar()

    def SchedReload(self):
        log.msg("Reloading Task Scheduler")
        self.taskman = taskman
        return self.taskman.reload()

# Twisted Application Framework setup:
application = service.Application('LISA')
LisaInstance = LisaFactory()

# Create a task manager to pass it to other services
taskman = ScheduledTaskManager(configuration)
scheduler = ScheduledTaskService(taskman)

# Environment setup for Django project files:
sys.path.append(os.path.normpath(os.path.join(os.path.abspath("."), "web")))
sys.path.append(os.path.normpath(os.path.join(os.path.abspath("."), "web/lisa")))
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.lisa.settings'

# Creating MultiService
multi = service.MultiService()
pool = threadpool.ThreadPool()
tps = ThreadPoolService(pool)
tps.setServiceParent(multi)

# Creating the web stuff
resource_wsgi = wsgi.WSGIResource(reactor, tps.pool, WSGIHandler())
root = libs.Root(resource_wsgi)
staticrsrc = static.File(os.path.normpath(os.path.join(os.path.abspath("."), "web/lisa/static")))
root.putChild("static", staticrsrc)

# Create the websocket
if configuration['enable_secure_mode']:
    socketfactory = WebSocketServerFactory("wss://" + configuration['lisa_url'] + ":" +\
                                       str(configuration['lisa_web_port_ssl']),debug=False)
else:
    socketfactory = WebSocketServerFactory("ws://" + configuration['lisa_url'] + ":" +\
                                       str(configuration['lisa_web_port']),debug=False)

socketfactory.protocol = libs.WebSocketProtocol
socketfactory.protocol.configuration, socketfactory.protocol.dir_path = configuration, dir_path
socketresource = WebSocketResource(socketfactory)
root.putChild("websocket", socketresource)

# Configuring servers to launch
if configuration['enable_secure_mode'] or configuration['enable_unsecure_mode']:
    if configuration['enable_secure_mode']:
        SSLContextFactoryEngine = ssl.DefaultOpenSSLContextFactory(
            os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.key'),
            os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.crt')
        )
        SSLContextFactoryWeb = ssl.DefaultOpenSSLContextFactory(
            os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.key'),
            os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.crt')
        )
        ctx = SSLContextFactoryEngine.getContext()
        ctx.set_verify(
            SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
            libs.verifyCallback
        )
        # Since we have self-signed certs we have to explicitly
        # tell the server to trust them.
        with open(os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.pem'), 'w') as outfile:
            for file in os.listdir(os.path.normpath(dir_path + '/' + 'Configuration/ssl/public/')):
                with open(os.path.normpath(dir_path + '/' + 'Configuration/ssl/public/'+file)) as infile:
                    for line in infile:
                        outfile.write(line)


        ctx.load_verify_locations(os.path.normpath(dir_path + '/' + 'Configuration/ssl/server.pem'))

        internet.SSLServer(configuration['lisa_web_port_ssl'],
                           server.Site(root), SSLContextFactoryWeb).setServiceParent(multi)
        internet.SSLServer(configuration['lisa_engine_port_ssl'],
                           LisaInstance, SSLContextFactoryEngine).setServiceParent(multi)

    if configuration['enable_unsecure_mode']:
        # Serve it up:
        internet.TCPServer(configuration['lisa_web_port'], server.Site(root)).setServiceParent(multi)
        internet.TCPServer(configuration['lisa_engine_port'], LisaInstance).setServiceParent(multi)
else:
    exit(1)
scheduler.setServiceParent(multi)
multi.setServiceParent(application)
