from models import Plugin, Description, Rule, Cron
import json, git
from shutil import rmtree
from twisted.python.reflect import namedAny
import inspect

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

def install(plugin_url=None, plugin_sha=None, plugin_name=None):
    if plugin_url and plugin_sha:
        repo = git.Repo.clone_from(plugin_url, LISA_PATH + '/plugins/' + plugin_name)
        repo.git.checkout(plugin_sha)
    metadata = json.load(open(LISA_PATH + '/plugins/' + plugin_name + '/' + str(plugin_name).lower() + '.json'))

    if Plugin.objects(name=plugin_name):
        return {'status': 'fail', 'log': 'Plugin already installed'}
    else:
        plugin = Plugin()
        description_list = []
        for item in metadata:
            if item != 'cron' or item != 'rules':
                if item == 'description':
                    for description in metadata[item]:
                        oDescription = Description()
                        for k,v in description.iteritems():
                            setattr(oDescription, k, v)
                        description_list.append(oDescription)
                    setattr(plugin, item, description_list)
                elif item == 'enabled':
                    if metadata[item] == 0:
                        setattr(plugin, item, False)
                    else:
                        setattr(plugin, item, True)
                else:
                    setattr(plugin, item, metadata[item])
        plugin.save()
        for item in metadata:
            if item == 'rules':
                for rule_item in metadata['rules']:
                    rule = Rule()
                    for parameter in rule_item:
                        setattr(rule, parameter, rule_item[parameter])
                    rule.plugin = plugin
                    rule.save()
            if item == 'crons':
                for cron_item in metadata['crons']:
                    cron = Cron()
                    for parameter in cron_item:
                        setattr(cron, parameter, cron_item[parameter])
                    cron.plugin = plugin
                    cron.save()
        return {'status': 'success', 'log': 'Plugin installed'}

def enable(plugin_name=None, plugin_pk=None):
    if plugin_pk:
        plugin_list = Plugin.objects(pk=plugin_pk)
    else:
        plugin_list = Plugin.objects(name=plugin_name)
    for plugin in plugin_list:
        if plugin.enabled:
            return {'status': 'fail', 'log': 'Plugin already enabled'}
        else:
            plugin.enabled = True
            plugin.save()
            for cron in Cron.objects(plugin=plugin):
                cron.enabled = True
                cron.save()
            for rule in Rule.objects(plugin=plugin):
                rule.enabled = True
                rule.save()
            return {'status': 'success', 'log': 'Plugin enabled'}

def disable(plugin_name=None, plugin_pk=None):
    if plugin_pk:
        plugin_list = Plugin.objects(pk=plugin_pk)
    else:
        plugin_list = Plugin.objects(name=plugin_name)
    for plugin in plugin_list:
        if not plugin.enabled:
            return {'status': 'fail', 'log': 'Plugin already disabled'}
        else:
            plugin.enabled = False
            plugin.save()
            for cron in Cron.objects(plugin=plugin):
                cron.enabled = False
                cron.save()
            for rule in Rule.objects(plugin=plugin):
                rule.enabled = False
                rule.save()
            return {'status': 'success', 'log': 'Plugin disabled'}


def uninstall(plugin_name=None, plugin_pk=None):
    if plugin_pk:
        plugin_list = Plugin.objects(pk=plugin_pk)
    else:
        plugin_list = Plugin.objects(name=plugin_name)
    if not plugin_list:
        return {'status': 'fail', 'log': 'Plugin not installed'}
    else:
        for plugin in plugin_list:
            rmtree(LISA_PATH + '/plugins/' + plugin['name'])
            plugin.delete()
            for cron in Cron.objects(plugin=plugin):
                cron.delete()
            for rule in Rule.objects(plugin=plugin):
                rule.delete()
        return {'status': 'success', 'log': 'Plugin uninstalled'}

def method_list(plugin_name=None):
    if plugin_name:
        plugin_list = Plugin.objects(name=plugin_name)
    else:
        plugin_list = Plugin.objects.all()
    listmethodplugins = []
    for plugin in plugin_list:
        plugininstance = namedAny('.'.join((str(plugin.name), 'modules', str(plugin.name).lower(),
                                            str(plugin.name))))()
        listmethods = []
        for m in inspect.getmembers(plugininstance, predicate=inspect.ismethod):
            if not "__init__" in m:
                listmethods.append(m[0])
        listmethodplugins.append({ 'plugin': plugin.name, 'methods': listmethods})
    return listmethodplugins