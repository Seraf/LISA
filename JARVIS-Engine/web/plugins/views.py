from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Plugin
import requests
import json

def index(request):
    modules = []
    repo = requests.get('https://api.github.com/repos/Seraf/JARVIS-Plugins/contents/')
    if(repo.ok):
        repoItems = json.loads(repo.text or repo.content)
        for item in repoItems:
            if(     item['type'] == 'dir' or \
                    (item['type'] == 'file' and 'Seraf/JARVIS-Plugins' not in item['git_url'])):
                
                for plugin in Plugin.objects(name=item['name']):
                    item['enabled'] = plugin.enabled
                modules.append(item)

    # Get all plugins from DB
    plugins = Plugin.objects
    return render_to_response('index.html', {'Plugins': plugins, 'RepoItems': modules},
                              context_instance=RequestContext(request))
