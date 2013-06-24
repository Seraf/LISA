from twisted.internet import reactor, threads
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import json

class LisaClient(Protocol):
    def sendMessage(self, message):
        self.transport.write(json.dumps( \
            {"from": 'Android',"type": 'Speech', "body": unicode(message), "zone": "Android"}))

    def dataReceived(self, data):
        print "data received"
        datajson = json.loads(data)
	print datajson

class LisaClientFactory(ReconnectingClientFactory):

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        self.protocol = LisaClient()
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

if __name__ == "__main__":
    # Start as a regular Python script.
    from twisted.internet import reactor
    LisaFactory = LisaClientFactory()
    lisaclient = reactor.connectTCP("127.0.0.1", 10042, LisaFactory)
    #reactor.callInThread(recognizeloop,LisaFactory)
    d = LisaFactory.login(
        cred.credentials.UsernamePassword('username', 'password'),
        client=self
    )
    d.addCallback(connected)
    d.addErrback(error)    
    reactor.run()
