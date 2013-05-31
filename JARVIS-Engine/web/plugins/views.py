from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from models import Plugin
import requests, json, git
from web.jarvis.utils import method_restricted_to, is_ajax
from web.jarvis.settings import JARVIS_PATH, APP_DIR, PROJECT_PATH


@method_restricted_to('GET')
def index(request):
    plugins = []
    metareq = requests.get('https://raw.github.com/Seraf/JARVIS-Plugins/master/plugin_list.json')
    if(metareq.ok):
        for item in json.loads(metareq.text or metareq.content):
            for plugin in Plugin.objects(name=item['name']):
                item['enabled'] = plugin.enabled
                if(plugin.version < item['enabled']):
                    item['upgrade'] = True
            plugins.append(item)
    return render_to_response('index.html', {'Plugins': plugins},
                              context_instance=RequestContext(request))

@is_ajax()
@method_restricted_to('POST')
def install(request):
    plugin_name = request.POST.get('name', '')
    plugin_url = request.POST.get('url', '')
    plugin_sha = request.POST.get('sha', '')
    repo = git.Repo.clone_from(plugin_url, JARVIS_PATH + '/Plugins/' + plugin_name)
    repo.git.checkout(plugin_sha)
    return HttpResponse('SUCCESS')
