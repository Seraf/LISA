import urllib, json
import xml.etree.ElementTree as ET

class Allocine:
    def __init__(self):
        pass

    def getFilms(self):

        configuration = ET.parse('Plugins/Configuration/allocine.xml').getroot()
        salles = configuration.find('salles')
        url = "http://api.allocine.fr/rest/v3/showtimelist?partner="+configuration.findtext('partner_id')+"&theaters="

        for salle in salles:
            url=url+salle.text+","

        allocineResponse = urllib.urlopen(url)
        allocineJson = json.load(allocineResponse)
        list_films_str = ""

        for cinema in allocineJson['feed']['theaterShowtimes']:
            list_films_str = list_films_str + "dans le cinema : "+cinema['place']['theater']['name']+", sont joues les films suivants : "
            first = True
            for film in cinema['movieShowtimes']:
                if first == False:
                    list_films_str = list_films_str + "puis "
                list_films_str = list_films_str + film['onShow']['movie']['title']+" "
                first = False
        return list_films_str
