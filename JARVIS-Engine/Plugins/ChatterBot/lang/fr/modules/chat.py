# -*- coding: UTF-8 -*-
from datetime import datetime
import json
from pymongo import MongoClient

class Chat:
    def __init__(self):
        self.configuration_jarvis = json.load(open('Configuration/jarvis.json'))
        mongo = MongoClient(self.configuration_jarvis['database']['server'],\
                            self.configuration_jarvis['database']['port'])
        self.configuration = mongo.jarvis.plugins.find_one({"name": "ChatterBot"})

    def getTime(self):
        now = datetime.now()
        return json.dumps({"plugin": "chat","method": "getTime", \
                           "body": now.strftime("Il est %HH%M")})