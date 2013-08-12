import json, re, sys
from pymongo import MongoClient
from twisted.python.reflect import namedAny

class RulesEngine():
    def __init__(self, configuration):
        self.configuration = configuration
        client = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = client.lisa
        self.build_default_schema()

    def build_default_schema(self):
        key_defaultanswer =     {   "name": "DefaultAnwser" }
        data_defaultanswer =    {
                                    "name": "DefaultAnwser",
                                    "order": 999,
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

        if self.configuration['debug']['debug_before_before_rule']:
            print "Before 'before' rule: " + str(jsonInput)
        for rule in rulescollection.find({"enabled": True, "before": {"$ne":None}}).sort([("order", 1)]):
            exec(rule['before'])
        if self.configuration['debug']['debug_after_before_rule']:
            print "After 'before' rule: " + str(jsonInput)
        oPlugin = pluginscollection.find_one({"configuration.intents."+jsonInput['outcome']['intent']: {"$exists": True}})
        if oPlugin:
            plugininstance = namedAny('.'.join((str(oPlugin["name"]),'modules',str(oPlugin["name"]).lower(),str(oPlugin["name"]))))()
            methodToCall = getattr(plugininstance, oPlugin['configuration']['intents'][jsonInput['outcome']['intent']]['method'])
            jsonOutput = methodToCall(jsonInput)
        else:
            jsonOutput = {}
            jsonOutput['plugin'] = "None"
            jsonOutput['method'] = "None"
            jsonOutput['body'] = "I don't know what to say"
        jsonOutput['from'] = jsonData['from']
        if self.configuration['debug']['debug_wit']:
            print "WIT: " + str(jsonOutput)
        if self.configuration['debug']['debug_before_after_rule']:
            print "Before 'after' rule: " + str(jsonOutput)
        for rule in rulescollection.find({"enabled": True, "after": {"$ne":None}}).sort([("order", 1)]):
            exec(rule['after'])
            #Problem here : it don't check if the condition of the rule after has matched to end the rules
            if rule['end']:
                break
        if self.configuration['debug']['debug_after_after_rule']:
            print "After 'after' rule: " + str(jsonOutput)
