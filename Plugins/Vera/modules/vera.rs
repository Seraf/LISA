> object gettemperature python
    import urllib, json
    import xml.etree.ElementTree as ET

    configuration = ET.parse('Plugins/Configuration/vera.xml').getroot()
    temperature = configuration.find('temperature')
    get = temperature.find('get')
    variables = get.find('variables')

    url = "http://"+configuration.findtext('ip')+":"+configuration.findtext('port')+"/data_request?id=status&output_format=json&DeviceNum="+temperature.findtext('device_number')
    veraResponse = urllib.urlopen(url)
    states = json.load(veraResponse)['Device_Num_'+temperature.findtext('device_number')]['states']

    for state in states:
        for variable in variables.findall('variable'):
            if state['variable'] == variable.text:
                return "Il fait "+state['value']+" degres"
< object