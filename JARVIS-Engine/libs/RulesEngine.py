import json, re
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
                                    "before": None,
                                    "after": "jarvisprotocol.transport.write(json.dumps(                     \
                                                    {                                                       \
                                                        'plugin': jsonAnswer['plugin'],                     \
                                                        'method': jsonAnswer['method'],                     \
                                                        'body': jsonAnswer['body'],                         \
                                                        'client_uuid': jarvisprotocol.client_uuid,          \
                                                        'from': jsonData['from']                            \
                                                    }))",
                                    "end": True,
                                    "enabled": True
                                }
        self.database.rules.update(key_defaultanswer, data_defaultanswer, upsert=True)

    def Rules(self, jsonData, jarvisprotocol):
        rulescollection = self.database.rules

        for rule in rulescollection.find({ "enabled": True, "before": {"$ne":None}}).sort([("order", 1)]):
            #jarvisprotocol.bot_library.k.freeze_uservars(user="localuser")
            reply = jarvisprotocol.bot_library.respond_to(user="localuser", text=str(jsonData['body'].encode('utf-8')))
            last = jarvisprotocol.bot_library.k.last_match(user="localuser")
            info = jarvisprotocol.bot_library.k.trigger_info(trigger=last)
            #jarvisprotocol.bot_library.k.thaw_uservars(user="localuser", action="thaw")
            filename = re.match(r"^.*/Plugins/(\w+)/.*", info[0]['filename']).group(1)
            try:
                jsonAnswer = json.loads(reply)
            except:
                jsonAnswer = json.loads(json.dumps({"plugin": filename,"method": None,"body": reply}))
            exec(rule['before'])

        #jarvisprotocol.bot_library.k.freeze_uservars(user="localuser")
        reply = jarvisprotocol.bot_library.respond_to(user="localuser", text=str(jsonData['body'].encode('utf-8')))
        last = jarvisprotocol.bot_library.k.last_match(user="localuser")
        info = jarvisprotocol.bot_library.k.trigger_info(trigger=last)
        #jarvisprotocol.bot_library.k.thaw_uservars(user="localuser", action="discard")
        filename = re.match(r"^.*/Plugins/(\w+)/.*", info[0]['filename']).group(1)
        try:
            jsonAnswer = json.loads(reply)
        except:
            jsonAnswer = json.loads(json.dumps({"plugin": filename,"method": None,"body": reply}))

        for rule in rulescollection.find({ "enabled": True, "after": {"$ne":None}}).sort([("order", 1)]):
            exec(rule['after'])
            #Problem here : it don't check if the condition of the rule after has matched to end the rules
            if rule['end']:
                break