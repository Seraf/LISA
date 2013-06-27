from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import ssl
from OpenSSL import SSL

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


