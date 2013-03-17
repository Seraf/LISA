> object getprogrammetv python
    import urllib
    import xml.etree.ElementTree as ET
    from datetime import timedelta, datetime, date
    import dateutil.parser
    import os, os.path

    configuration = ET.parse('Plugins/Configuration/programmetv.xml').getroot()

    url = "http://www.kazer.org/tvguide.xml?u="+configuration.findtext('user_id')
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
    return programmetv_str
< object