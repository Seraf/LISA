from twisted.words.protocols.jabber.jid import JID
from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol, AvailablePresence
from wokkel import client, xmppim

class JarvisBotProtocol(MessageProtocol):
    def connectionMade(self):
        print "Connected!"

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
            reply.addElement("body", content="echo: " + str(msg.body))

            self.send(reply)


jid = JID("jarvis.systeme@gmail.com/JARVIS")
secret = 'jarvispowered'

xmppClient = client.XMPPClient(jid, secret)
xmppClient.logTraffic = True

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
    application = service.Application("XMPP Client")
    jarvisbot = JarvisBotProtocol()
    jarvisbot.setHandlerParent(xmppClient)
    xmppClient.setServiceParent(application)