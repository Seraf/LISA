> object gettrains python
import urllib, json
import xml.etree.ElementTree as ET

configuration = ET.parse('Plugins/Configuration/sncf.xml').getroot()
url = "http://www.transilien.com/flux/rss/trafic"
sncfResponse = urllib.urlopen(url)

for ligne in lignes:
    channel -> item -> title

< object