from tastypie import authorization
from tastypie_mongoengine import resources
from django.conf.urls.defaults import *
import json
from libs import LisaInstance, Lisa

try:
    from web.lisa.settings import LISA_PATH
except ImportError:
    from lisa.settings import LISA_PATH


class LisaResource(resources.MongoEngineResource):
    class Meta:
        allowed_methods = ('get', 'post')
        authorization = authorization.Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/engine/reload$" % (self._meta.resource_name),
                self.wrap_view('engine_reload'), name="api_lisa_engine_reload"),
            url(r"^(?P<resource_name>%s)/scheduler/reload" % (self._meta.resource_name),
                self.wrap_view('scheduler_reload'), name="api_lisa_scheduler_reload"),
            url(r"^(?P<resource_name>%s)/speak" % (self._meta.resource_name),
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
        self.method_check(request, allowed=['post'])
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
        self.method_check(request, allowed=['post'])
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
