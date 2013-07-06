from tastypie import authorization
from django.conf.urls.defaults import *
import json
from tastypie import resources
from tastypie.utils import trailing_slash

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

class Interface(object):
    def __init__(self):
        return None

class InterfaceResource(resources.Resource):
    class Meta:
        resource_name = 'interface'
        allowed_methods = ()
        authorization = authorization.Authorization()
        object_class = Interface
        extra_actions = [
            {
                'name': 'dashboard/widget/list',
                'http_method': 'GET',
                'fields': {}
            },
            {
                'name': 'dashboard/widget/add',
                'http_method': 'POST',
                'fields': {}
            },
            {
                'name': 'dashboard/widget/delete',
                'http_method': 'POST',
                'fields': {}
            },
        ]

    def base_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_schema'), name="api_get_schema"),

            url(r"^(?P<resource_name>%s)/dashboard/widget/add%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('widget_add'), name="api_widget_add"),
            url(r"^(?P<resource_name>%s)/dashboard/widget/delete%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('widget_delete'), name="api_widget_delete"),
            url(r"^(?P<resource_name>%s)/dashboard/widget/list%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('widget_list'), name="api_widget_list"),

        ]

    def list(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        #try:
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'log': "List"}, HttpAccepted)

    def add(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        #try:
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'log': "Add"}, HttpAccepted)

    def delete(self, request, **kwargs):
        self.method_check(request, allowed=['delete'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        #try:
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'log': "Delete"}, HttpAccepted)


    def engine_reload(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            LisaInstance.LisaReload()
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'log': "L.I.S.A Engine reloaded"}, HttpAccepted)

    def scheduler_reload(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            LisaInstance.SchedReload()
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'log': "L.I.S.A Task Scheduler reloaded"},
                                    HttpAccepted)

    def get_object_list(self, request):
        return [Lisa()]