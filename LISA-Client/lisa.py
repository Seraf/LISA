from twisted.internet import ssl, reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import json, os

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
configuration = json.load(open(os.path.normpath(dir_path + '/' + 'Configuration/lisa.json')))

class LisaClient(Protocol):
    def sendMessage(self, message):
        self.transport.write(json.dumps(
            {"from": 'Android',"type": 'Speech', "body": unicode(message), "zone": "Android"})
        )

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

class CtxFactory(ssl.ClientContextFactory):
    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.use_certificate_file(os.path.normpath(dir_path + '/' + 'Configuration/ssl/client.crt'))
        ctx.use_privatekey_file(os.path.normpath(dir_path + '/' + 'Configuration/ssl//client.key'))

        return ctx

if __name__ == "__main__":
    # Start as a regular Python script.
    LisaFactory = LisaClientFactory()

    if configuration['enable_secure_mode']:
        from OpenSSL import SSL
        reactor.connectSSL(configuration['lisa_url'], configuration['lisa_engine_port_ssl'], LisaFactory, CtxFactory())

    else:
        lisaclient = reactor.connectTCP(configuration['lisa_url'], configuration['lisa_engine_port'], LisaFactory)

    reactor.run()