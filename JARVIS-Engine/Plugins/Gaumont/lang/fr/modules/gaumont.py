# -*- coding: UTF-8 -*-
import urllib, json
from bs4 import BeautifulSoup

class Gaumont:
    def __init__(self):
        pass

    def getFilms(self):
        film_str = ""
        configuration = json.load(open('Plugins/Configuration/gaumont.json'))
        for salle in configuration['salles']:
            film_str += u" Dans la salle "+ salle['name'] +u" sont joués les films : "
            soup = BeautifulSoup(urllib.urlopen(configuration['url']+salle['id']))
            film_str += u' puis '.join(unicode(film.get_text()) for film in soup.find_all("p", class_="titre"))
        return film_str