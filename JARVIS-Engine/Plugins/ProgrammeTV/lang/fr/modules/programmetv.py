# -*- coding: UTF-8 -*-
import urllib, json
import xml.etree.ElementTree as ET
from datetime import date
import os

class ProgrammeTV:
    def __init__(self):
        pass

    def getProgrammeTV(self):
        configuration = json.load(open('Plugins/Configuration/programmetv.json'))

        url = "http://www.kazer.org/tvguide.xml?u="+configuration['user_id']
        kazerResponse = urllib.urlopen(url)
        if not os.path.exists('tmp/'+str(date.today())+'_programmetv.xml'):
            print "Downloading the tv program"
            import glob
            files=glob.glob('tmp/*_programmetv.xml')
            for filename in files:
                os.unlink(filename)
            urllib.urlretrieve(url,'tmp/'+str(date.today())+'_programmetv.xml')
        programmetv = ET.parse('tmp/'+str(date.today())+'_programmetv.xml').getroot()

        channelDict = {}
        programmetv_str = ""
        for child in programmetv:
            if child.tag == "channel":
                channelDict[child.attrib['id']] = child.find('display-name').text
            if child.tag == "programme":
                if date.today().strftime("%Y%m%d")+"2045" <= child.attrib['start'][:12] and date.today().strftime("%Y%m%d")+"2200" > child.attrib['start'][:12]:
                    programmetv_str = programmetv_str + 'Sur '+channelDict[child.attrib['channel']]+' a '+ child.attrib['start'][8:10] + ' heure ' + child.attrib['start'][10:12] + ' il y a : '+ child.find('title').text+'. '
        return json.dumps({"plugin": "programmetv","method": "getProgrammeTV", \
                           "body": programmetv_str})