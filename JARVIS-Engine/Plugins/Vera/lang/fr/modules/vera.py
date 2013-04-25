import urllib, json

class Vera:
    def __init__(self):
        pass

    def getTemperature(self, args):
        configuration = json.load(open('Plugins/Configuration/vera.json'))
        for device in configuration['temperature']:
            url = "http://"+configuration['ip']+":"+configuration['port']+"/data_request?id=status&output_format=json&DeviceNum="+device['device_id']
            veraResponse = urllib.urlopen(url)
            states = json.load(veraResponse)['Device_Num_'+device['device_id']]['states']
        for state in states:
            for variable in device['variables']:
                if state['variable'] == variable.text:
                    return u"Il fait "+state['value']+u" degrés"