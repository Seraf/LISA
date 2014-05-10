# -*- coding: UTF-8 -*-
import os
import json
import sys
import uuid
from lisa.server.libs import RulesEngine, Commands
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import ssl
from twisted.python import log
from OpenSSL import SSL
from lisa.server.libs.txscheduler.manager import ScheduledTaskManager
from lisa.server.libs.txscheduler.service import ScheduledTaskService
from lisa.server.plugins.PluginManager import PluginManagerSingleton

from lisa.server.service import configuration, dir_path
from lisa.server.web.manageplugins.models import Intent, Rule

# Create a task manager to pass it to other services
taskman = ScheduledTaskManager(configuration)
scheduler = ScheduledTaskService(taskman)


class ServerTLSContext(ssl.DefaultOpenSSLContextFactory):
    def __init__(self, *args, **kw):
        kw['sslmethod'] = SSL.TLSv1_METHOD
        ssl.DefaultOpenSSLContextFactory.__init__(self, *args, **kw)


class Lisa(LineReceiver):
    def __init__(self,factory):
        self.factory = factory

    def answerToClient(self, jsondata):
        if configuration['debug']['debug_output']:
            log.msg("OUTPUT: " + str(jsondata))
        jsonreturned = json.loads(jsondata)
        if 'all' in jsonreturned['clients_zone']:
            for client in self.factory.clients:
                client['object'].sendLine(jsondata)
        else:
            for zone in jsonreturned['clients_zone']:
                if zone == 'sender':
                    self.sendLine(jsondata)
                else:
                    for client in self.factory.clients:
                        if client['zone'] == zone:
                            client['object'].sendLine(jsondata)

    def askToClient(self, jsondata):
        jsondata['type'] = 'question'
        self.answerToClient(jsondata=jsondata)

    def connectionMade(self):
        self.client_uuid = str(uuid.uuid1())
        self.factory.clients.append({"object": self, "zone": "", "type": "", "uuid": self.client_uuid})
        if configuration['enable_secure_mode']:
            ctx = ServerTLSContext(
                privateKeyFileName=os.path.normpath(dir_path + '/' + 'configuration/ssl/server.key'),
                certificateFileName= os.path.normpath(dir_path + '/' + 'configuration/ssl/server.crt')
            )
            self.transport.startTLS(ctx, self.factory)
            pass

    def connectionLost(self, reason):
        log.err('Lost connection.  Reason:', reason)
        for client in self.factory.clients:
            if client['object'] == self:
                self.factory.clients.remove(client)

    def lineReceived(self, data):
        if configuration['debug']['debug_input']:
            log.msg("INPUT: " + str(data))
        try:
            jsonData = json.loads(data)
        except ValueError, e:
            self.sendLine("Error : Invalid JSON")
        else:
            for client in self.factory.clients:
                if client['object'] == self and (not client['type'] or not client['zone']):
                    client['type'], client['zone'] = jsonData['type'], jsonData['zone']
            if jsonData['type'] == "chat":
                RulesEngine(configuration).Rules(jsonData=jsonData, lisaprotocol=self)
            elif jsonData['type'] == "command":
                Commands(configuration, lisaprotocol=self).parse(jsonData=jsonData)


class LisaFactory(Factory):
    def __init__(self):
        self.clients = []
        self.syspath = sys.path

    def buildProtocol(self, addr):
        self.Lisa = Lisa(self)
        return self.Lisa

    def LisaReload(self):
        global enabled_plugins
        log.msg("Reloading L.I.S.A Engine")
        sys.path = self.syspath
        enabled_plugins = []
        self.build_activeplugins()

    def SchedReload(self):
        global taskman
        log.msg("Reloading Task Scheduler")
        self.taskman = taskman
        return self.taskman.reload()


class LisaProtocolSingleton(object):
    """
    Singleton version of the Lisa Protocol.

    Being a singleton, this class should not be initialised explicitly
    and the ``get`` classmethod must be called instead.
    """

    __instance = None

    def __init__(self):
        """
        Initialisation: this class should not be initialised
        explicitly and the ``get`` classmethod must be called instead.
        """

        if self.__instance is not None:
            raise Exception("Singleton can't be created twice !")

    def get(self):
        """
        Actually create an instance
        """
        if self.__instance is None:
            self.__instance = Lisa(LisaFactorySingleton.get())
            log.msg("LisaProtocol initialised")
        return self.__instance
    get = classmethod(get)


class LisaFactorySingleton(object):
    """
    Singleton version of the Lisa Factory.

    Being a singleton, this class should not be initialised explicitly
    and the ``get`` classmethod must be called instead.
    """

    __instance = None

    def __init__(self):
        """
        Initialisation: this class should not be initialised
        explicitly and the ``get`` classmethod must be called instead.
        """

        if self.__instance is not None:
            raise Exception("Singleton can't be created twice !")

    def get(self):
        """
        Actually create an instance
        """
        if self.__instance is None:
            self.__instance = LisaFactory()
            log.msg("LisaFactory initialised")
        return self.__instance
    get = classmethod(get)


# Create an instance of factory, then create a protocol instance to import it everywhere
LisaFactorySingleton.get()
LisaProtocolSingleton.get()

# Load the plugins
PluginManagerSingleton.get().loadPlugins()


def Initialize():
    # Create the default core_intents_list intent
    defaults_intent_list = {'name': "core_intents_list",
                     'function': "list",
                     'module': "lisa.server.core.intents.Intents",
                     'enabled': True
    }

    intent_list, created = Intent.objects.get_or_create(name='core_intents_list', defaults=defaults_intent_list)

    # Create the default rule of the rule engine
    defaults_rule = {'name': "DefaultAnwser",
                     'order': 999,
                     'before': None,
                     'after': """lisaprotocol.answerToClient(json.dumps(
                                                {
                                                    'plugin': jsonOutput['plugin'],
                                                    'method': jsonOutput['method'],
                                                    'body': jsonOutput['body'],
                                                    'clients_zone': ['sender'],
                                                    'from': jsonOutput['from']
                                                }))""",
                     'end': True,
                     'enabled': True
    }
    default_rule, created = Rule.objects.get_or_create(name='DefaultAnwser', defaults=defaults_rule)