from tastypie import authorization
from django.conf.urls.defaults import *
import json
from libs import LisaInstance, Lisa
from tastypie import resources
from tastypie.utils import trailing_slash

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH

class Lisa(object):
    def __init__(self):
        return None

class LisaResource(resources.Resource):
    class Meta:
        resource_name = 'lisa'
        allowed_methods = ()
        authorization = authorization.Authorization()
        object_class = Lisa
        extra_actions = [
            {
                'name': 'engine/reload',
                'http_method': 'GET',
                'fields': {}
            },
            {
                'name': 'scheduler/reload',
                'http_method': 'GET',
                'fields': {}
            },
            {
                'name': 'speak',
                'http_method': 'POST',
                'fields':{
                    'message': {
                        'type': 'string',
                        'required': True,
                        'description': 'The message to transmit to client(s)'
                    },
                    'clients_zone': {
                        'type': 'list',
                        'required': True,
                        'description': "Provide a list of zones : ['all','WebSocket','Bedroom'] ..."
                    }
                }
            }
        ]

    def base_urls(self):
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_schema'), name="api_get_schema"),

            url(r"^(?P<resource_name>%s)/engine/reload%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('engine_reload'), name="api_lisa_engine_reload"),
            url(r"^(?P<resource_name>%s)/scheduler/reload%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('scheduler_reload'), name="api_lisa_scheduler_reload"),
            url(r"^(?P<resource_name>%s)/speak%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('speak'), name="api_lisa_speak"),
        ]

    def speak(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        #try:
        message = request.POST.get("message")
        clients_zone = request.POST.getlist("clients_zone")
        jsondata = json.dumps({
                                      'body': message,
                                      'clients_zone': clients_zone,
                                      'from': "API"
            })
        Lisa(LisaInstance, LisaInstance.bot_library).answerToClient(jsondata=jsondata)

        #except:
        #    pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'log': "Message sent"}, HttpAccepted)

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