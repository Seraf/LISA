# -*- coding: UTF-8 -*-
from twisted.words.protocols.jabber.jid import JID
from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol, AvailablePresence
from wokkel import client, xmppim
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import json
import xml.etree.ElementTree as ET

configuration = ET.parse('Configuration/Gtalk.xml').getroot()
account = configuration.find('account')
whitelist = configuration.find('whitelist')
botname = configuration.find('botname')

class LisaClient(Protocol):
    def __init__(self, LisaBotProtocol):
        self.LisaBotProtocol = LisaBotProtocol
    def sendMessage(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        self.LisaBotProtocol.sendAnswer(data)

class LisaClientFactory(ReconnectingClientFactory):
    def __init__(self, LisaBotProtocol):
        self.LisaBotProtocol = LisaBotProtocol
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        self.protocol = LisaClient(self.LisaBotProtocol)
        print 'Connected to Lisa.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

class LisaBotProtocol(MessageProtocol):
    def connectionMade(self):
        self.lisaclientfactory = LisaClientFactory(self)
        print "Connected!"
        lisaclient = reactor.connectTCP("localhost", 10042, self.lisaclientfactory)
        # send initial presence
        self.send(AvailablePresence())

    def connectionLost(self, reason):
        print "Disconnected!"

    def sendAnswer(self,data):
        jsonData = json.loads(data)
        print jsonData
        reply = domish.Element((None, "message"))
        reply["to"] = jsonData["from"]
        reply["type"] = "chat"
        reply.addElement("body", content=unicode(jsonData["body"]))
        self.send(reply)

    def onMessage(self, msg):
        for id in whitelist:
            if msg["type"] == 'chat' and hasattr(msg, "body") and msg.body is not None and id.text in msg['from']:
                self.lisaclientfactory.protocol.sendMessage(json.dumps( \
                    {"from": msg["from"],"type": msg["type"], "body": unicode(msg.body), "zone": "Gtalk"}))

jid = JID(account[0].text+"/"+botname.text)
secret = account[1].text

xmppClient = client.XMPPClient(jid, secret)
xmppClient.logTraffic = False

if __name__ == "__main__":
    # Start as a regular Python script.

    import sys
    from twisted.python import log
    from twisted.internet import reactor
    log.startLogging(sys.stdout, setStdout=0)
    lisabot = LisaBotProtocol()
    lisabot.setHandlerParent(xmppClient)
    xmppClient.startService()
    reactor.run()
else:
    # Start as a Twisted Application
    from twisted.application import service
    application = service.Application("LisaTalkBot")
    lisabot = LisaBotProtocol()
    lisabot.setHandlerParent(xmppClient)
    xmppClient.setServiceParent(application)