import json
from pymongo import MongoClient

class RulesEngine():
    def __init__(self, configuration):
        client = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = client.jarvis
        self.build_default_schema()

    def build_default_schema(self):
        key_defaultanswer =     {   "name": "DefaultAnwser" }
        data_defaultanswer =    {
                                    "name": "DefaultAnwser",    \
                                    "order": 999,               \
                                    "conditions": [
                                                    {
                                                        "if": '1',                  \
                                                        "operator": '==',           \
                                                        "compare": '1',             \
                                                    }
                                                  ],
                                    "then": "jarvisprotocol.transport.write(json.dumps(                     \
                                                    {                                                       \
                                                        'plugin': jsonAnswer['plugin'],                     \
                                                        'method': jsonAnswer['method'],                     \
                                                        'body': jsonAnswer['body'],                         \
                                                        'client_uuid': jarvisprotocol.client_uuid,          \
                                                        'from': jsonData['from']                            \
                                                    }))",       \
                                    "end": True
                                }
        self.database.rules.update(key_defaultanswer, data_defaultanswer, upsert=True)

    def Rules(self, jsonData, jsonAnswer, jarvisprotocol):
        rulescollection = self.database.rules
        for rule in rulescollection.find().sort([("order", 1)]):
            # should build a if string by recursively parsing conditions
            # condition = self.build_condition(conditions=rule['conditions'])
            for condition in rule['conditions']:
                condition_string = 'if ' + condition['if'] + ' ' + condition['operator'] + ' ' +            \
                                   condition['compare'] + ': '
                exec(condition_string + rule['then'])
            if rule['end']:
                break