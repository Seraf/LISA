import json, os, gettext
from pymongo import MongoClient
import lisa.server

class Commands():
    """
        body : contains the text that will be spoken
        type : will be "command"
        from : the message is issued from "LISA Server"
        command : contains the command name
        clients_zone : should be ['sender'] to answer to the client who issued the command,
        * : you can pass other parameters in your json. The client will handle these as he recognize the command name

    """

    def __init__(self, configuration, lisaprotocol):
        self.configuration = configuration
        client = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = client.lisa

        path = os.path.normpath(str(lisa.server.__path__[0]) + "/lang")
        self._ = translation = gettext.translation(domain='lisa', localedir=path, fallback=True,
                                              languages=[self.configuration['lang']]).ugettext
        self.lisaprotocol = lisaprotocol

    def mute(self, clientList):
        # ask clients to mute
        # TODO should be fixed, it's not good json to send
        if 'all' in clientList:
            for client in self.lisaprotocol.factory.clients:
                client['object'].sendLine("{'body': 'mute', 'from': 'LISA Server', 'type': 'command'}")
        else:
            for zone in clientList:
                for client in self.lisaprotocol.factory.clients:
                    if client['zone'] == zone:
                            client['object'].sendLine("{'body': 'mute', 'from': 'LISA Server', 'type': 'command'}")

    def parse(self, jsonData):
        if jsonData['body'] == 'LOGIN':
            self.lisaprotocol.answerToClient(json.dumps(
                {
                    'body': self._('The client %(from)s has joined the zone %(zone)s') %
                            {'from': jsonData['from'], 'zone': jsonData['zone']},
                    'command': 'LOGIN',
                    'clients_zone': ['sender'],
                    'from': 'LISA Server',
                    'type': 'command',
                    'bot_name': self.configuration['bot_name']
                }
            ))
        else:
            print jsonData