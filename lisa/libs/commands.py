import json, re, sys, os, inspect, gettext
from pymongo import MongoClient
from twisted.python.reflect import namedAny
from twisted.python import log

class Commands():
    def __init__(self, configuration, lisaprotocol):
        self.configuration = configuration
        client = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = client.lisa
        path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
        inspect.getfile(inspect.currentframe()))[0],os.path.normpath("lang/"))))
        self._ = translation = gettext.translation(domain='lisa', localedir=path, languages=[self.configuration['lang']]).ugettext
        self.lisaprotocol = lisaprotocol

    def mute(self, clientList):
        #ask clients to mute
        #
        if 'all' in clientList:
            for client in self.lisaprotocol.factory.clients:
                client['object'].sendLine("{'body': 'mute', 'from': 'LISA Server', 'type': 'command'}")
        else:
            for zone in clientList:
                for client in self.lisaprotocol.factory.clients:
                    if client['zone'] == zone:
                            client['object'].sendLine("{'body': 'mute', 'from': 'LISA Server', 'type': 'command'}")

    def parse(self, jsonData):
        pass