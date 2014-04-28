from tastypie import authorization
from tastypie.utils import trailing_slash
from tastypie_mongoengine import resources, fields
from lisa.server.web.manageplugins.models import Plugin, Description, Rule, Intent
from django.conf.urls import *
from lisa.server.libs import LisaInstance, Lisa
from lisa.server.libs.server import pluginmanager
from tastypie.http import HttpAccepted, HttpNotModified, HttpCreated


class PluginResource(resources.MongoEngineResource):
    description = fields.EmbeddedListField(of='lisa.server.web.manageplugins.api.EmbeddedDescriptionResource',
                                           attribute='description', full=True, null=True)
    class Meta:
        queryset = Plugin.objects.all()
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()
        extra_actions = [
            {
                'name': 'install',
                'summary': 'Install a plugin',
                'http_method': 'POST',
                "errorResponses": [
                    {
                      "reason": "Plugin was installed correctly.",
                      "code": 201
                    },
                    {
                      'reason': "There was a problem during the install.",
                      'code': 304
                    }
                ],
                'fields':{}
            },
            {
                'name': 'uninstall',
                'summary':'Uninstall a plugin',
                'http_method': 'GET',
                'fields':{}
            },
            {
                'name': 'enable',
                'summary':'Enable a plugin',
                'http_method': 'GET',
                'fields':{}
            },
            {
                'name': 'disable',
                'summary':'Disable a plugin',
                'http_method': 'GET',
                'fields':{}
            },
            {
                'name': 'methodslist',
                'summary':'List the method of all (or the plugin name in parameter) plugins installed',
                'http_method': 'GET',
                'fields':{}
            },
        ]

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<plugin_name>[\w_-]+)/install%s" % (self._meta.resource_name,
                                                                                trailing_slash()),
                self.wrap_view('install'), name="api_plugin_install"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/enable%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('enable'), name="api_plugin_enable"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/disable%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('disable'), name="api_plugin_disable"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/uninstall%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('uninstall'), name="api_plugin_uninstall"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/upgrade%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('upgrade'), name="api_plugin_upgrade"),
            url(r"^(?P<resource_name>%s)/(?P<plugin_name>[\w_-]+)/methodslist%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('methodslist'), name="api_plugin_methodslist"),
            url(r"^(?P<resource_name>%s)/methodslist%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('methodslist'), name="api_plugin_methodslist"),
        ]

    def install(self, request, **kwargs):
        self.method_check(request, allowed=['post','get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        plugin_name = kwargs['plugin_name']
        status = pluginmanager.installPlugin(plugin_name=plugin_name)

        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()
        return self.create_response(request, status, HttpCreated)


    def enable(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        status = pluginmanager.enablePlugin(plugin_pk=kwargs['pk'])
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()
        return self.create_response(request, status, HttpAccepted)

    def disable(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        status = pluginmanager.enablePlugin(plugin_pk=kwargs['pk'])
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()

        return self.create_response(request, status, HttpAccepted)

    def uninstall(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        status = pluginmanager.uninstallPlugin(plugin_pk=kwargs['pk'])
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()
        return self.create_response(request, status, HttpAccepted)

    def methodslist(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        if 'plugin_name' in kwargs:
            methods = pluginmanager.methodListPlugin(plugin_name=kwargs['plugin_name'])
        else:
            methods = pluginmanager.methodListPlugin()
        self.log_throttled_access(request)
        return self.create_response(request, methods, HttpAccepted)


class EmbeddedDescriptionResource(resources.MongoEngineResource):
    class Meta:
        object_class = Description
        allowed_methods = ('get')
        authorization = authorization.Authorization()

class IntentResource(resources.MongoEngineResource):
    plugin = fields.ReferenceField(to='lisa.server.web.manageplugins.api.PluginResource', attribute='plugin', null=True)

    class Meta:
        object_class = Intent
        authorization = authorization.Authorization()
