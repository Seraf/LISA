# -*- coding: UTF-8 -*-
import urllib, json
from bs4 import BeautifulSoup

class Cinema:
    def __init__(self):
        pass

    def getFilms(self):
        film_str = ""
        configuration = json.load(open('Plugins/Configuration/cinema.json'))
        for salle in configuration['salles']:
            if salle['enabled'] == 'True':
                film_str += u" Dans la salle "+ salle['name'] +u" sont joués les films : "
                #lxml improve speed but need to be installed
                #soup = BeautifulSoup(urllib.urlopen(configuration['url_' + salle['type']] + salle['id']),"lxml")
                soup = BeautifulSoup(urllib.urlopen(configuration['url_' + salle['type']] + salle['id']))
                if salle['type'] == "Gaumont":
                    film_str += u' puis '.join(unicode(film.get_text()) for film in soup.find_all("p", class_="titre"))
        return json.dumps({"plugin": "Cinema","method": "getFilms", \
                           "body": film_str})
