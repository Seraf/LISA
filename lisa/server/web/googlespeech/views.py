from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lisa.server.service import configuration

@login_required()
def index(request):
    if configuration['enable_secure_mode']:
        websocket = 'wss'
    else:
        websocket = 'ws'
    context = {'websocket': websocket}
    return render(request, 'googlespeech/index.html', context)
