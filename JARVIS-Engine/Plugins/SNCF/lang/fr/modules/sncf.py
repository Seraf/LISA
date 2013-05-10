# -*- coding: UTF-8 -*-
import urllib, json
from bs4 import BeautifulSoup
from pymongo import MongoClient

class SNCF:
    def __init__(self):
        self.configuration_jarvis = json.load(open('Configuration/jarvis.json'))
        mongo = MongoClient(self.configuration_jarvis['database']['server'], \
                            self.configuration_jarvis['database']['port'])
        self.configuration = mongo.jarvis.plugins.find_one({"name": "SNCF"})

    def getTrains(self):
        #lxml improve speed but need to be installed
        #soup = BeautifulSoup(urllib.urlopen(configuration['url'],"lxml"))
        soup = BeautifulSoup(urllib.urlopen(self.configuration['configuration']['url']))
        list_problemRSS = soup.find_all("title")
        list_problem_filter = []
        for problem in list_problemRSS:
            for ligne in self.configuration['configuration']['lignes']:
                if ligne['name'] in problem.get_text() and ligne['enabled'] == 'True':
                    list_problem_filter.append(unicode(problem.get_text()))
        if not list_problem_filter:
            return json.dumps({"plugin": "sncf","method": "getTrains", \
                               "body": u'Miracle, aucun problème à signaler'})
        else:
            return json.dumps({"plugin": "sncf","method": "getTrains", \
                               "body": u' puis '.join(list_problem_filter)})