from lisa.server.libs.server import LisaFactorySingleton
from twisted.trial import unittest
from twisted.test import proto_helpers

import json

class LisaClientTestCase(unittest.TestCase):
    def setUp(self):
        factory = LisaFactorySingleton.get()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def convertjson(self, type=None, message=None, command=None, argdict=None, zone="zone1"):
        jsondict = {"from": "TestClient"}
        if message:
            jsondict['body'] = unicode(message)
        if type:
            jsondict['type'] = type
        if command:
            jsondict['command'] = command
        if command:
            jsondict['command'] = command
        if zone:
            jsondict['zone'] = zone
        if argdict:
            for k,v in argdict.items():
                jsondict[k] = v

        return json.dumps(jsondict)

    #def test_receivechat(self):
    #    json = self.convertjson(message="")

    def test_receive_command_login(self):
        message = "LOGIN"
        argdict = {}
        datajson = self.convertjson(message=message, type="command", command="LOGIN", argdict=argdict, zone="zone1")
        self.proto.lineReceived(data=datajson)
        answer = json.loads(self.tr.value())
        self.assertEqual(answer['bot_name'], "lisa")
