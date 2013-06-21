from twisted.internet.protocol import Protocol, ReconnectingClientFactory


class LisaClient(Protocol):
    def __init__(self, WebSocketProtocol):
        self.WebSocketProtocol = WebSocketProtocol

    def sendMessage(self, msg):
        self.transport.write(msg)

    def dataReceived(self, data):
        self.WebSocketProtocol.sendMessage(data)

class LisaClientFactory(ReconnectingClientFactory):
    def __init__(self, WebSocketProtocol):
        self.WebSocketProtocol = WebSocketProtocol

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        self.protocol = LisaClient(self.WebSocketProtocol)
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


