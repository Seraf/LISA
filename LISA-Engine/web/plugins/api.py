from tastypie import authorization
from tastypie_mongoengine import resources, fields
from models import Plugin, Description, Rule, Cron
from django.conf.urls.defaults import *
import json, git, lisa
from shutil import rmtree

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH


class PluginResource(resources.MongoEngineResource):
    description = fields.EmbeddedListField(of='plugins.api.EmbeddedDescriptionResource',
                                           attribute='description', full=True, null=True)
    class Meta:
        queryset = Plugin.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<plugin_name>[\w_-]+)/install$" % (self._meta.resource_name),
                self.wrap_view('install'), name="api_plugin_install"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/enable$" % (self._meta.resource_name),
                self.wrap_view('enable'), name="api_plugin_enable"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/disable$" % (self._meta.resource_name),
                self.wrap_view('disable'), name="api_plugin_disable"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/uninstall$" % (self._meta.resource_name),
                self.wrap_view('uninstall'), name="api_plugin_uninstall"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/upgrade$" % (self._meta.resource_name),
                self.wrap_view('upgrade'), name="api_plugin_upgrade"),
            ]

    def install(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpCreated, HttpNotModified

        try:
            plugin_url = request.POST.get("url")
            plugin_sha = request.POST.get("sha")
            plugin_name = kwargs['plugin_name']
            repo = git.Repo.clone_from(plugin_url, LISA_PATH + '/Plugins/' + plugin_name)
            repo.git.checkout(plugin_sha)
            metadata = json.load(open(LISA_PATH + '/Plugins/' + plugin_name + '/' + str(plugin_name).lower() + '.json'))
            plugin = Plugin()
            for item in metadata:
                if item != 'cron' or item != 'rules':
                    setattr(plugin, item, metadata[item])
            plugin.save(validate=False)
            for item in metadata:
                if item == 'rules':
                    for rule_item in metadata['rules']:
                        rule = Rule()
                        for parameter in rule_item:
                            setattr(rule, parameter, rule_item[parameter])
                        rule.plugin = plugin
                        rule.save(validate=False)
                if item == 'crons':
                    for cron_item in metadata['crons']:
                        cron = Cron()
                        for parameter in cron_item:
                            setattr(cron, parameter, cron_item[parameter])
                        cron.plugin = plugin
                        cron.save(validate=False)
        except:
            pass
        #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        lisa.LisaInstance.SchedReload()
        lisa.LisaInstance.LisaReload()
        return self.create_response(request, { 'status': 'success', 'log': "Plugin Installed"}, HttpCreated)

    def enable(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            for plugin in Plugin.objects(pk=kwargs['pk']):
                plugin.enabled = True
                plugin.save()
                for cron in Cron.objects(plugin=plugin):
                    cron.enabled = True
                    cron.save()
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        lisa.LisaInstance.SchedReload()
        lisa.LisaInstance.LisaReload()
        return self.create_response(request, { 'status': 'success', 'log': "Plugin Enabled"}, HttpAccepted)

    def disable(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            for plugin in Plugin.objects(pk=kwargs['pk']):
                plugin.enabled = False
                plugin.save()
                for cron in Cron.objects(plugin=plugin):
                    cron.enabled = False
                    cron.save()
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        lisa.LisaInstance.SchedReload()
        lisa.LisaInstance.LisaReload()
        return self.create_response(request, { 'status': 'success', 'log': "Plugin Disabled"}, HttpAccepted)

    def uninstall(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            for plugin in Plugin.objects(pk=kwargs['pk']):
                rmtree(LISA_PATH + '/Plugins/' + plugin['name'])
                plugin.delete()
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        lisa.LisaInstance.SchedReload()
        lisa.LisaInstance.LisaReload()
        return self.create_response(request, { 'status': 'success', 'log': "Plugin Deleted"}, HttpAccepted)


class EmbeddedDescriptionResource(resources.MongoEngineResource):
    class Meta:
        object_class = Description
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
