from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lisa.server.ConfigManager import ConfigManagerSingleton

configuration = ConfigManagerSingleton.get().getConfiguration()

from pkg_resources import get_distribution

@login_required()
def index(request):
    if configuration['enable_secure_mode']:
        websocket = 'wss'
    else:
        websocket = 'ws'
    context = {
        'websocket': websocket,
        'lang': configuration['lang'],
        'server_version': get_distribution('lisa-server').version
    }
    return render(request, 'googlespeech/index.html', context)
