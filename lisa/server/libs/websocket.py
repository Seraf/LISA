from twisted.python import log
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.protocols.basic import Int32StringReceiver, LineReceiver
from OpenSSL import SSL
import os
import json
from twisted.internet import reactor, ssl
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

class CtxFactory(ssl.ClientContextFactory):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.use_certificate_file(os.path.normpath(self.dir_path + '/' + 'configuration/ssl/public/websocket.crt'))
        ctx.use_privatekey_file(os.path.normpath(self.dir_path + '/' + 'configuration/ssl/websocket.key'))
        return ctx


class WebSocketProtocol(WebSocketServerProtocol):
    def connectionMade(self):
        self.configuration = self.configuration
        WebSocketServerProtocol.connectionMade(self)
        self.lisaclientfactory = LisaClientFactory(self)
        if self.configuration['enable_secure_mode']:
             self.conn = reactor.connectSSL(self.configuration['lisa_url'], self.configuration['lisa_engine_port_ssl'],
                                            self.lisaclientfactory, CtxFactory()
             )
        else:
            self.conn = reactor.connectTCP(self.configuration['lisa_url'],
                                           self.configuration['lisa_engine_port'], self.lisaclientfactory)

    def onMessage(self, msg, binary):
        self.lisaclientfactory.protocol.sendMessage(json.dumps(
            {"from": "Lisa-Web","type": "chat", "body": unicode(msg.decode('utf-8')), "zone": "WebSocket"}))

    def connectionLost(self, reason):
        self.conn.transport = None


class ClientTLSContext(ssl.ClientContextFactory):
    isClient = 1
    def getContext(self):
        return SSL.Context(SSL.TLSv1_METHOD)


class LisaClient(LineReceiver):
    def __init__(self, WebSocketProtocol,factory):
        self.WebSocketProtocol = WebSocketProtocol
        self.factory = factory

    def sendMessage(self, msg):
        self.sendLine(msg)

    def lineReceived(self, data):
        self.WebSocketProtocol.sendMessage(data)

    def connectionMade(self):
        if self.WebSocketProtocol.configuration['enable_secure_mode']:
            ctx = ClientTLSContext()
            self.transport.startTLS(ctx, self.factory)

class LisaClientFactory(ReconnectingClientFactory):
    def __init__(self, WebSocketProtocol):
        self.WebSocketProtocol = WebSocketProtocol

    def startedConnecting(self, connector):
        log.msg('Started to connect.')

    def buildProtocol(self, addr):
        self.protocol = LisaClient(self.WebSocketProtocol, factory=self)
        log.msg('Connected to Lisa.')
        log.msg('Resetting reconnection delay')
        self.resetDelay()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        log.err('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        log.err('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


