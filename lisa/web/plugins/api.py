from tastypie import authorization
from tastypie.utils import trailing_slash
from tastypie_mongoengine import resources, fields
from models import Plugin, Description, Rule, Cron
from django.conf.urls import *
import json, git
from libs import LisaInstance, Lisa
from shutil import rmtree
import functions
try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH


class PluginResource(resources.MongoEngineResource):
    description = fields.EmbeddedListField(of='plugins.api.EmbeddedDescriptionResource',
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
                'fields':{
                    'url': {
                        'type': 'string',
                        'required': True,
                        'description': 'The url of the repository'
                    },
                    'sha': {
                        'type': 'string',
                        'required': True,
                        'description': "The sha of the plugin (to reference a commit)"
                    }
                }
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
        ]

    def install(self, request, **kwargs):
        self.method_check(request, allowed=['post','get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpCreated, HttpNotModified

        try:
            plugin_url = request.POST.get("url")
            plugin_sha = request.POST.get("sha")
            plugin_name = kwargs['plugin_name']
            status = functions.install(plugin_url=plugin_url, plugin_sha=plugin_sha, plugin_name=plugin_name)
        except:
            pass
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()
        return self.create_response(request, status, HttpCreated)


    def enable(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            status = functions.enable(plugin_pk=kwargs['pk'])
        except:
            pass
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()
        return self.create_response(request, status, HttpAccepted)

    def disable(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            status = functions.enable(plugin_pk=kwargs['pk'])
        except:
            pass
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()

        return self.create_response(request, status, HttpAccepted)

    def uninstall(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            status = functions.uninstall(plugin_pk=kwargs['pk'])
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        LisaInstance.SchedReload()
        LisaInstance.LisaReload()
        return self.create_response(request, status, HttpAccepted)


class EmbeddedDescriptionResource(resources.MongoEngineResource):
    class Meta:
        object_class = Description
        allowed_methods = ('get')
        authorization = authorization.Authorization()
