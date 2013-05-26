from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Plugin

def index(request):
    # Get all plugins from DB
    plugins = Plugin.objects
    return render_to_response('index.html', {'Plugins': plugins},
                              context_instance=RequestContext(request))
