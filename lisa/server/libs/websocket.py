from twisted.python import log
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from OpenSSL import SSL
import os
import json
from twisted.internet import reactor, ssl
from twisted.internet.protocol import Protocol
import gettext
from lisa.server.ConfigManager import ConfigManagerSingleton

configuration = ConfigManagerSingleton.get().getConfiguration()
path = ''.join([ConfigManagerSingleton.get().getPath(), '/lang/'])
_ = translation = gettext.translation(domain='lisa', localedir=path, fallback=True,
                                              languages=[configuration['lang']]).ugettext


class CtxFactory(ssl.ClientContextFactory):
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.use_certificate_file(os.path.normpath(self.dir_path + '/' + 'configuration/ssl/public/websocket.crt'))
        ctx.use_privatekey_file(os.path.normpath(self.dir_path + '/' + 'configuration/ssl/websocket.key'))
        return ctx


class WebSocketProtocol(Protocol):
    def connectionMade(self):
        self.lisaclientfactory = LisaClientFactory(self)
        if configuration['enable_secure_mode']:
            self.conn = reactor.connectSSL(configuration['lisa_url'], configuration['lisa_engine_port_ssl'],
                                           self.lisaclientfactory, CtxFactory())
        else:
            self.conn = reactor.connectTCP(configuration['lisa_url'],
                                           configuration['lisa_engine_port'], self.lisaclientfactory)

    def sendMessage(self, message):
        self.transport.write(message)

    def dataReceived(self, data):
        print data
        self.lisaclientfactory.protocol.sendMessage(json.dumps(
            {'from': 'Lisa-Web', 'type': 'chat', 'body': unicode(data), 'zone': 'WebSocket'}))

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
        if configuration['enable_secure_mode']:
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
        log.err("Lost connection.  Reason: %(reason)s" % {'reason': str(reason)})
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        log.err("Connection failed. Reason: %(reason)s" % {'reason': str(reason)})
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


