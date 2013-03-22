import os
import sys
import fnmatch
import libs
import xml.etree.ElementTree as ET

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Jarvis(LineReceiver):
    def __init__(self, bot_library):
        self.bot_library = bot_library

    def connectionLost(self, reason):
        print reason

    def lineReceived(self, line):
        self.sendLine(str(self.bot_library.respond_to(str(line.encode("utf-8"))).encode("utf-8")))


class JarvisFactory(Factory):

    def __init__(self):
        #Loading Jarvis
        try:
            self.bot_library = libs.RiveScriptBot()
            print "Successfully loaded bot"
        except:
            print "Couldn't load bot"

        for root, dirnames, filenames in os.walk('Plugins'):
            for filename in fnmatch.filter(filenames, '*.rs'):
                configuration = ET.parse('Plugins/Configuration/jarvis.xml').getroot()
                if 'lang/'+configuration.findtext('lang') in root or filename=='begin.rs':
                    self.bot_library.learn(root)

    def buildProtocol(self, addr):
        return Jarvis(self.bot_library)


reactor.listenTCP(10042, JarvisFactory())
reactor.run()