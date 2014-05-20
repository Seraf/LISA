from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Plugin
from django.contrib.auth.decorators import login_required
import requests, json
from lisa.server.web.weblisa.utils import method_restricted_to

from pkg_resources import get_distribution

@method_restricted_to('GET')
@login_required()
def list(request):
    plugins = []
    metareq = requests.get('http://plugins.lisa-project.net/plugins.json')
    if(metareq.ok):
        for item in json.loads(metareq.text or metareq.content):
            for plugin in Plugin.objects(name=item['name']):
                item['id'] = plugin.id
                item['enabled'] = plugin.enabled
                if plugin.version < item['version']:
                    item['upgrade'] = True
            #if os.path.exists(LISA_PATH + '/Plugins/' + item['name']):
            #    item['installed'] = True
            plugins.append(item)
    return render_to_response('list.html', {'Plugins': plugins,
                                            'server_version': get_distribution('lisa-server').version},
                              context_instance=RequestContext(request))
