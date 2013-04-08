# -*- coding: UTF-8 -*-
import os
import fnmatch
import libs
import xml.etree.ElementTree as ET
import json
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from apscheduler.scheduler import Scheduler

class Jarvis(Protocol):
    def __init__(self, bot_library):
        self.bot_library = bot_library

    def connectionLost(self, reason):
        print 'Lost connection.  Reason:', reason

    def dataReceived(self, data):
        jsonData = json.loads(data)
        answerbody = self.bot_library.respond_to(str(jsonData['body'].encode('utf-8')))
        self.transport.write(json.dumps({"from": jsonData["from"],"type": jsonData["type"],"body": answerbody}))

class JarvisFactory(Factory):

    def __init__(self):
        try:
            self.bot_library = libs.RiveScriptBot()
            print "Successfully loaded bot"
        except:
            print "Couldn't load bot"

        for root, dirnames, filenames in os.walk('Plugins'):
            for filename in fnmatch.filter(filenames, '*.rs'):
                configuration = ET.parse('Plugins/Configuration/jarvis.xml').getroot()
                if os.path.normpath('lang/'+configuration.findtext('lang')) in root or filename=='begin.rs':
                    self.bot_library.learn(root)

    def buildProtocol(self, addr):
        return Jarvis(self.bot_library)


scheduler = Scheduler()
scheduler.start()

reactor.listenTCP(10042, JarvisFactory())
reactor.run()
