from twisted.words.protocols.jabber.jid import JID
from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol, AvailablePresence
from wokkel import client, xmppim
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import json
from sys import stdout

class JarvisClient(Protocol):
    def sendMessage(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print "Server said:", data

class JarvisClientFactory(ReconnectingClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        self.protocol = JarvisClient()
        print 'Connected to Jarvis.'
        print 'Resetting reconnection delay'
        self.resetDelay()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

class JarvisBotProtocol(MessageProtocol):
    def connectionMade(self):
        self.jarvisclientfactory = JarvisClientFactory()
        print "Connected!"
        jarvisclient = reactor.connectTCP("localhost", 10042, self.jarvisclientfactory)
        # send initial presence
        self.send(AvailablePresence())

    def connectionLost(self, reason):
        print "Disconnected!"

    def onMessage(self, msg):
        if msg["type"] == 'chat' and hasattr(msg, "body") and msg.body is not None:


            reply = domish.Element((None, "message"))
            reply["to"] = msg["from"]
            #reply["from"] = msg["to"]
            reply["type"] = 'chat'

            self.jarvisclientfactory.protocol.sendMessage(json.dumps({"from": msg["from"],"type": msg["type"], "body": str(msg.body)})) #str(msg.body)}))
            #reply.addElement("body", content="echo: " + str(msg.body))

            #self.send(reply)


jid = JID("jarvis.systeme@gmail.com/JARVIS")
secret = 'jarvispowered'

xmppClient = client.XMPPClient(jid, secret)
xmppClient.logTraffic = False

if __name__ == "__main__":
    # Start as a regular Python script.

    import sys
    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout, setStdout=0)



    jarvisbot = JarvisBotProtocol()
    jarvisbot.setHandlerParent(xmppClient)


    xmppClient.startService()
    reactor.run()
else:
    # Start as a Twisted Application

    from twisted.application import service
    application = service.Application("JarvisTalkBot")
    jarvisbot = JarvisBotProtocol()
    jarvisbot.setHandlerParent(xmppClient)
    xmppClient.setServiceParent(application)