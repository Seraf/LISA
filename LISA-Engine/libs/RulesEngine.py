import json, re, sys
from pymongo import MongoClient
from twisted.python.reflect import namedAny

class RulesEngine():
    def __init__(self, configuration):
        client = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = client.lisa
        self.build_default_schema()

    def build_default_schema(self):
        key_defaultanswer =     {   "name": "DefaultAnwser" }
        data_defaultanswer =    {
                                    "name": "DefaultAnwser",    \
                                    "order": 999,               \
                                    "before": None,
                                    "after": "lisaprotocol.answerToClient(json.dumps(                       \
                                                    {                                                       \
                                                        'plugin': jsonOutput['plugin'],                     \
                                                        'method': jsonOutput['method'],                     \
                                                        'body': jsonOutput['body'],                         \
                                                        'clients_zone': ['sender'],                         \
                                                        'from': jsonOutput['from']                          \
                                                    }))",
                                    "end": True,
                                    "enabled": True
                                }
        self.database.rules.update(key_defaultanswer, data_defaultanswer, upsert=True)

    def Rules(self, jsonData, lisaprotocol):
        rulescollection = self.database.rules
        pluginscollection = self.database.plugins

        jsonInput = lisaprotocol.wit.message_send(str(jsonData['body'].encode('utf-8')))
        jsonInput['from'], jsonInput['type'], jsonInput['zone'] = jsonData['from'], jsonData['type'], jsonData['zone']

        for rule in rulescollection.find({"enabled": True, "before": {"$ne":None}}).sort([("order", 1)]):
            exec(rule['before'])

        oPlugin = pluginscollection.find_one({"configuration.intents."+jsonInput['outcome']['intent']: {"$exists": True}})
        plugininstance = namedAny('.'.join((str(oPlugin["name"]),'modules',str(oPlugin["name"]).lower(),str(oPlugin["name"]))))()
        methodToCall = getattr(plugininstance, oPlugin['configuration']['intents'][jsonInput['outcome']['intent']]['method'])
        jsonOutput = methodToCall(jsonInput)
        jsonOutput['from'] = jsonData['from']

        print jsonOutput
        for rule in rulescollection.find({ "enabled": True, "after": {"$ne":None}}).sort([("order", 1)]):
            exec(rule['after'])
            #Problem here : it don't check if the condition of the rule after has matched to end the rules
            if rule['end']:
                break