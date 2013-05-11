# -*- coding: UTF-8 -*-
import json
from pymongo import MongoClient
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api
from time import time

class SNMP:
    def __init__(self):
        self.startedAt = time()
        # Protocol version to use
        self.pMod = api.protoModules[api.protoVersion2c]
        # Build PDU
        self.reqPDU = self.pMod.SetRequestPDU()

    def cbTimerFun(self, timeNow):
        if timeNow - self.startedAt > 3:
            raise Exception("Request timed out")

    def cbRecvFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg):
        while wholeMsg:
            rspMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=self.pMod.Message())
            rspPDU = self.pMod.apiMessage.getPDU(rspMsg)
            # Match response to request
            if self.pMod.apiPDU.getRequestID(self.reqPDU) == self.pMod.apiPDU.getRequestID(rspPDU):
                # Check for SNMP errors reported
                errorStatus = self.pMod.apiPDU.getErrorStatus(rspPDU)
                if errorStatus:
                    print(errorStatus.prettyPrint())
                transportDispatcher.jobFinished(1)
        return wholeMsg

    def send(self, host, community, oid, value):
        self.pMod.apiPDU.setDefaults(self.reqPDU)
        self.pMod.apiPDU.setVarBinds(
            self.reqPDU,
            ((oid, self.pMod.OctetString(value)),
            )
        )

        # Build message
        reqMsg = self.pMod.Message()
        self.pMod.apiMessage.setDefaults(reqMsg)
        self.pMod.apiMessage.setCommunity(reqMsg, community)
        self.pMod.apiMessage.setPDU(reqMsg, self.reqPDU)

        transportDispatcher = AsynsockDispatcher()
        transportDispatcher.registerRecvCbFun(self.cbRecvFun)
        transportDispatcher.registerTimerCbFun(self.cbTimerFun)

        # UDP/IPv4
        transportDispatcher.registerTransport(
            udp.domainName, udp.UdpSocketTransport().openClientMode()
        )

        # Pass message to dispatcher
        transportDispatcher.sendMessage(
            encoder.encode(reqMsg), udp.domainName, (host, 161)
        )
        transportDispatcher.jobStarted(1)

        # Dispatcher will finish as job#1 counter reaches zero
        transportDispatcher.runDispatcher()
        transportDispatcher.closeDispatcher()


class BBox:
    def __init__(self):
        self.configuration_jarvis = json.load(open('Configuration/jarvis.json'))
        mongo = MongoClient(self.configuration_jarvis['database']['server'], \
                            self.configuration_jarvis['database']['port'])
        self.configuration = mongo.jarvis.plugins.find_one({"name": "BBox"})
        self.snmp = SNMP()
        self.chaines = {
            "une": ["50"],
            "deux": ["51"],
            "trois": ["52"],
            "quatre": ["53"],
            "cinq": ["54"],
            "six": ["55"],
            "sept": ["56"],
            "huit": ["57"],
            "neuf": ["58"],
            "dix": ["50","59"],
            "onze": ["50","50"],
            "douze": ["50","51"],
        }

    def change_channel(self, args):
        number = str(args[0]).strip()
        for chaine in self.chaines[number]:
            self.snmp.send( host=str(self.configuration['configuration']['ip']),                \
                            community=str(self.configuration['configuration']['community']),    \
                            oid=str(self.configuration['configuration']['oid']),                \
                            value=str(chaine)
            )
        return json.dumps({ "plugin": "BBox","method": "change_channel",                        \
                            "body": u"Chaine changée"})

    def change_volume(self, args):
        return json.dumps({ "plugin": "BBox","method": "change_volume",                         \
                            "body": ""})

    def rec_channel(self, args):
        return json.dumps({ "plugin": "BBox","method": "rec_channel",                           \
                            "body": ""})

    def pause_channel(self, args):
        return json.dumps({ "plugin": "BBox","method": "pause_channel",                         \
                            "body": ""})