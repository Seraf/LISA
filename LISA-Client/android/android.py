import androidhelper
from twisted.internet import reactor, threads
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
import json

droid = androidhelper.Android()

class LisaClient(Protocol):
    def sendMessage(self, message):
        self.transport.write(json.dumps( \
            {"from": 'Android',"type": 'Speech', "body": unicode(message), "zone": "Android"}))

    def dataReceived(self, data):
        print "data received"
        datajson = json.loads(data)
        droid.ttsSpeak(datajson['body'])

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

def recognizeloop(LisaFactory):
    while 1:
        # Using Android API for Google Voice and Recognizing command
        #data = droid.recognizeSpeech().result
        # Command is open or close proceding it to the Server else Error message
        #print "Should listen LISA : "
        #print data
        #if data == "Lisa":
        if not droid.ttsIsSpeaking()[1]:
            message = droid.recognizeSpeech().result
            # Sending command
            print "MESSAGE : "
            print message
            if message == "Sortie" or message == "Exit":
                reactor.callFromThread(reactor.stop)
            reactor.callFromThread(LisaFactory.protocol.sendMessage, message)

if __name__ == "__main__":
    # Start as a regular Python script.
    from twisted.internet import reactor
    LisaFactory = LisaClientFactory()
    lisaclient = reactor.connectTCP("192.168.1.80", 10042, LisaFactory)
    reactor.callInThread(recognizeloop,LisaFactory)
    reactor.run()