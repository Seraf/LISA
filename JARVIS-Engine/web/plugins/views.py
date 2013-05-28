from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Plugin
import requests
import json, base64

def index(request):
    plugins = []
    metareq = requests.get('https://raw.github.com/Seraf/JARVIS-Plugins/master/plugin_list.json')
    if(metareq.ok):
        for item in json.loads(metareq.text or metareq.content):
            for plugin in Plugin.objects(name=item['name']):
                item['enabled'] = plugin.enabled
            plugins.append(item)
    return render_to_response('index.html', {'Plugins': plugins},
                              context_instance=RequestContext(request))
