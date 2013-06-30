from tastypie import authorization
from tastypie_mongoengine import resources, fields
from models import Plugin, Description
from django.conf.urls.defaults import *
from tastypie.utils import trailing_slash

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
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/remove$" % (self._meta.resource_name),
                self.wrap_view('remove'), name="api_plugin_remove"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/upgrade$" % (self._meta.resource_name),
                self.wrap_view('upgrade'), name="api_plugin_upgrade"),
            ]

    from tastypie.http import HttpCreated, HttpNotModified

    def install(self, request, **kwargs):
        self.method_check(request, allowed=['post','get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            output = kwargs['plugin_name']
        except:
            pass
        #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        return self.create_response(request, { 'status' : 'success', 'log' : output })


class EmbeddedDescriptionResource(resources.MongoEngineResource):
    class Meta:
        object_class = Description
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = authorization.Authorization()
