> object getprogrammetv python
import urllib
import xml.etree.ElementTree as ET

configuration = ET.parse('Plugins/Configuration/programmetv.xml').getroot()

url = "http://www.kazer.org/tvguide.xml?u="+configuration.findtext('user_id')
kazerResponse = urllib.urlopen(url)

< object