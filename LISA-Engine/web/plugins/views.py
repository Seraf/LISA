from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from models import Plugin, Rule, Cron
import requests, json, git, os
from shutil import rmtree
from lisa.utils import method_restricted_to, is_ajax
from lisa.settings import LISA_PATH

@method_restricted_to('GET')
def index(request):
    plugins = []
    metareq = requests.get('https://raw.github.com/Seraf/LISA-Plugins/master/plugin_list.json')
    if(metareq.ok):
        for item in json.loads(metareq.text or metareq.content):
            for plugin in Plugin.objects(name=item['name']):
                item['enabled'] = plugin.enabled
                if plugin.version < item['version']:
                    item['upgrade'] = True
            if os.path.exists(LISA_PATH + '/Plugins/' + item['name']):
                item['installed'] = True
            plugins.append(item)
    return render_to_response('index.html', {'Plugins': plugins},
                              context_instance=RequestContext(request))

@is_ajax()
@method_restricted_to('POST')
def enable(request):
    plugin_name = request.POST.get('name', '')
    for plugin in Plugin.objects(name=plugin_name):
        plugin.enabled = True
        plugin.save()
        for cron in Cron.objects(plugin=plugin):
            cron.enabled = True
            cron.save()
    return HttpResponse('OK')

@is_ajax()
@method_restricted_to('POST')
def disable(request):
    plugin_name = request.POST.get('name', '')
    for plugin in Plugin.objects(name=plugin_name):
        plugin.enabled = False
        plugin.save()
        for cron in Cron.objects(plugin=plugin):
            cron.enabled = False
            cron.save()
    return HttpResponse('OK')

@is_ajax()
@method_restricted_to('POST')
def uninstall(request):
    plugin_name = request.POST.get('name', '')
    for plugin in Plugin.objects(name=plugin_name):
        plugin.delete()
    rmtree(LISA_PATH + '/Plugins/' + plugin_name)
    return HttpResponse('OK')


@is_ajax()
@method_restricted_to('POST')
def install(request):
    plugin_name = request.POST.get('name', '')
    plugin_url = request.POST.get('url', '')
    plugin_sha = request.POST.get('sha', '')
    repo = git.Repo.clone_from(plugin_url, LISA_PATH + '/Plugins/' + plugin_name)
    repo.git.checkout(plugin_sha)
    metadata = json.load(open(LISA_PATH + '/Plugins/' + plugin_name + '/' + str(plugin_name).lower() + '.json'))
    plugin = Plugin()
    for item in metadata:
        if item != 'cron' or item != 'rules':
            setattr(plugin, item, metadata[item])
    plugin.save(validate=False)
    for item in metadata:
        if item == 'rule':
            for rule_item in metadata['rule']:
                rule = Rule()
                for parameter in rule_item:
                    setattr(rule, parameter, rule_item[parameter])
                rule.plugin = plugin
                rule.save(validate=False)
        if item == 'cron':
            for cron_item in metadata['cron']:
                cron = Cron()
                for parameter in cron_item:
                    setattr(cron, parameter, cron_item[parameter])
                cron.plugin = plugin
                cron.save(validate=False)
    return HttpResponse('OK')
