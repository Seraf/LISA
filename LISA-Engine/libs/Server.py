# -*- coding: UTF-8 -*-
import os,json,sys,uuid
import libs
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import ssl
from twisted.python import log
from pymongo import MongoClient
from OpenSSL import SSL
from libs.txscheduler.manager import ScheduledTaskManager
from libs.txscheduler.service import ScheduledTaskService

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path) + '/../'
configuration = json.load(open(os.path.normpath(dir_path + '/' + 'Configuration/lisa.json')))

# Create a task manager to pass it to other services
taskman = ScheduledTaskManager(configuration)
scheduler = ScheduledTaskService(taskman)


class ServerTLSContext(ssl.DefaultOpenSSLContextFactory):
    def __init__(self, *args, **kw):
        kw['sslmethod'] = SSL.TLSv1_METHOD
        ssl.DefaultOpenSSLContextFactory.__init__(self, *args, **kw)

class Lisa(Protocol):
    def __init__(self,factory, bot_library):
        self.factory = factory
        self.bot_library = bot_library

    def answerToClient(self, jsondata):
        jsonreturned = json.loads(jsondata)
        for zone in jsonreturned['clients_zone']:
            for client in self.factory.clients:
                if client['zone'] == zone or zone == 'all':
                    client['object'].transport.write(jsondata)

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
            plugin_module_path = str(os.path.normpath(dir_path + '/Plugins/' + plugin['name'] + '/modules/'))
            plugin_web_path = str(os.path.normpath(dir_path + '/Plugins/' + plugin['name'] + '/web/'))
            if os.path.exists(plugin_module_path):
                sys.path.append(plugin_module_path)
            if os.path.exists(plugin_web_path):
                sys.path.append(plugin_web_path)
            self.bot_library.learn(os.path.normpath(dir_path + '/' + 'Plugins/' + plugin['name'] + '/lang/' +
                                                    configuration['lang'] + '/'))

    def buildProtocol(self, addr):
        self.Lisa = Lisa(self,self.bot_library)
        return self.Lisa

    def LisaReload(self):
        log.msg("Reloading L.I.S.A Engine")
        sys.path = self.syspath
        self.build_grammar()

    def SchedReload(self):
        global taskman
        log.msg("Reloading Task Scheduler")
        self.taskman = taskman
        return self.taskman.reload()

LisaInstance = LisaFactory()
