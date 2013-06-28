from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from OpenSSL import SSL
import os,libs,json
from twisted.internet import reactor, ssl
from autobahn.websocket import WebSocketServerProtocol

class CtxFactory(ssl.ClientContextFactory):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.use_certificate_file(os.path.normpath(self.dir_path + '/' + 'Configuration/ssl/public/websocket.crt'))
        ctx.use_privatekey_file(os.path.normpath(self.dir_path + '/' + 'Configuration/ssl/websocket.key'))
        return ctx

class WebSocketProtocol(WebSocketServerProtocol):
    def connectionMade(self):
        self.configuration = self.configuration
        WebSocketServerProtocol.connectionMade(self)
        self.lisaclientfactory = libs.LisaClientFactory(self)
        if self.configuration['enable_secure_mode']:
             reactor.connectSSL(self.configuration['lisa_url'], self.configuration['lisa_engine_port_ssl'],
                                self.lisaclientfactory, CtxFactory()
             )
        else:
            reactor.connectTCP(self.configuration['lisa_url'],
                               self.configuration['lisa_engine_port'], self.lisaclientfactory)

    def onMessage(self, msg, binary):
        self.lisaclientfactory.protocol.sendMessage(json.dumps(
            {"from": "Lisa-Web","type": "Chat", "body": unicode(msg.decode('utf-8')), "zone": "WebSocket"}))


class ClientTLSContext(ssl.ClientContextFactory):
    isClient = 1
    def getContext(self):
        return SSL.Context(SSL.TLSv1_METHOD)

class LisaClient(Protocol):
    def __init__(self, WebSocketProtocol,factory):
        self.WebSocketProtocol = WebSocketProtocol
        self.factory = factory

    def sendMessage(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        self.WebSocketProtocol.sendMessage(data)

    def connectionMade(self):
        if self.WebSocketProtocol.configuration['enable_secure_mode']:
            ctx = ClientTLSContext()
            self.transport.startTLS(ctx, self.factory)

class LisaClientFactory(ReconnectingClientFactory):
    def __init__(self, WebSocketProtocol):
        self.WebSocketProtocol = WebSocketProtocol

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        self.protocol = LisaClient(self.WebSocketProtocol, factory=self)
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


