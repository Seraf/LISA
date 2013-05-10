
# -*- coding: UTF-8 -*-
import json
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

class Izipedia:
    def __init__(self):
        self.configuration_jarvis = json.load(open('Configuration/jarvis.json'))
        mongo = MongoClient(self.configuration_jarvis['database']['server'], \
                            self.configuration_jarvis['database']['port'])
        self.configuration = mongo.jarvis.plugins.find_one({"name": "Izipedia"})

    def ask_izipedia(self, args):
	question = " ".join(args)
        data = dict(self.configuration['configuration'].items() + {'question': question}.items())
        req = requests.post("http://izipedia.com/api_tester.php", data)
        page = json.loads(req.content)
        return json.dumps({"plugin": "izipedia","method": "ask_izipedia", \
	                   "body": "".join(BeautifulSoup(page['long_text']).findAll(text=True)) })
