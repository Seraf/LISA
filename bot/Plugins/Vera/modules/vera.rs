> object temperature python
    import urllib, json
    url = "http://192.168.1.100:3480/data_request?id=status&output_format=json&DeviceNum=6"
    veraResponse = urllib.urlopen(url)
    states = json.load(veraResponse)['Device_Num_6']['states']

    for state in states:
        if state['variable'] == 'CurrentTemperature':
            return "Il fait "+state['value']+" degres"
< object