from twisted.internet import ssl, reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.python import log
import json, os
from OpenSSL import SSL

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
configuration = json.load(open(os.path.normpath(dir_path + '/' + 'Configuration/lisa.json')))

class LisaClient(LineReceiver):
    def __init__(self,factory):
        self.factory = factory

    def sendMessage(self, message):
        self.sendLine(json.dumps(
            {"from": 'Linux',"type": 'Speech', "body": unicode(message), "zone": "Android"})
        )
    def lineReceived(self, data):
        log.msg("data received")
        datajson = json.loads(data)
        log.msg(datajson)

    def connectionMade(self):
        log.msg('Connected to Lisa.')
        if configuration['enable_secure_mode']:
            ctx = ClientTLSContext()
            self.transport.startTLS(ctx, self.factory)

class LisaClientFactory(ReconnectingClientFactory):
    def startedConnecting(self, connector):
        log.msg('Started to connect.')

    def buildProtocol(self, addr):
        self.protocol = LisaClient(self)
        log.msg('Resetting reconnection delay')
        self.resetDelay()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        log.err('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        log.err('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

class ClientTLSContext(ssl.ClientContextFactory):
    isClient = 1
    def getContext(self):
        return SSL.Context(SSL.TLSv1_METHOD)

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
        reactor.connectSSL(configuration['lisa_url'], configuration['lisa_engine_port_ssl'], LisaFactory, CtxFactory())
    else:
        lisaclient = reactor.connectTCP(configuration['lisa_url'], configuration['lisa_engine_port'], LisaFactory)

    reactor.run()
