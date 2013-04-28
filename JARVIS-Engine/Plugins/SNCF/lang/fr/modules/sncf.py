# -*- coding: UTF-8 -*-
import urllib, json
from bs4 import BeautifulSoup

class SNCF:
    def __init__(self):
        pass

    def getTrains(self):
        configuration = json.load(open('Plugins/Configuration/sncf.json'))
        #lxml improve speed but need to be installed
        #soup = BeautifulSoup(urllib.urlopen(configuration['url'],"lxml"))
        soup = BeautifulSoup(urllib.urlopen(configuration['url']))
        list_problemRSS = soup.find_all("title")
        list_problem_filter = []
        for problem in list_problemRSS:
            for ligne in configuration['lignes']:
                if ligne['name'] in problem.get_text() and ligne['enabled'] == 'True':
                    list_problem_filter.append(unicode(problem.get_text()))
        if not list_problem_filter:
            return json.dumps({"plugin": "sncf","method": "getTrains", \
                               "body": u'Miracle, aucun problème à signaler'})
        else:
            return json.dumps({"plugin": "sncf","method": "getTrains", \
                               "body": u' puis '.join(list_problem_filter)})