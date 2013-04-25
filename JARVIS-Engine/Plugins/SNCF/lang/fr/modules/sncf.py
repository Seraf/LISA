# -*- coding: UTF-8 -*-
import urllib, json
from bs4 import BeautifulSoup

class SNCF:
    def __init__(self):
        pass

    def getTrains(self):
        configuration = json.load(open('Plugins/Configuration/sncf.json'))
        soup = BeautifulSoup(urllib.urlopen(configuration['url']), "lxml")
        list_problemRSS = soup.find_all("title")
        list_problem_filter = []
        for problem in list_problemRSS:
            for ligne in configuration['lignes']:
                if ligne['name'] in problem.get_text() and ligne['enabled'] == 'True':
                    list_problem_filter.append(unicode(problem.get_text()))
        if not list_problem_filter:
            return u'Miracle, aucun problème à signaler'
        else:
            return u' puis '.join(list_problem_filter)