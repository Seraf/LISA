from lisaserver.libs.server import LisaFactory
from twisted.trial import unittest
from twisted.test import proto_helpers

import json
import platform


class LisaClientTestCase(unittest.TestCase):
    def setUp(self):
        factory = LisaFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def convertjson(self, type=None, message=None, command=None, argdict=None):
        jsondict = {"from": "LISA Server"}
        if message:
            jsondict['body'] = unicode(message)
        if type:
            jsondict['type'] = type
        if command:
            jsondict['command'] = command
        if argdict:
            for k,v in argdict.items():
                jsondict[k] = v

        return json.dumps(jsondict)

    #def test_receivechat(self):
    #    json = self.convertjson(message="")


    def test_receive_command_login(self):
        message = "The client " + unicode(platform.node()) + " joined the zone"
        argdict = {"bot_name": "test", "nolistener": True}
        json = self.convertjson(message=message, type="command", command="LOGIN", argdict=argdict)
        self.proto.lineReceived(data=json)
        self.assertEqual(self.proto.bot_name, "test")
