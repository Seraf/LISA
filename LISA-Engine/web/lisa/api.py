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
            },
            {
                'name': 'tts/google',
                'http_method': 'POST',
                'fields':{
                    'message': {
                        'type': 'string',
                        'required': True,
                        'description': 'The message to vocalize'
                    },
                    'lang': {
                        'type': 'string',
                        'required': True,
                        'description': "Lang of the message"
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
            url(r"^(?P<resource_name>%s)/tts/google%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('tts_google'), name="api_lisa_tts_google"),
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


    def tts_google(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified
        import re
        import requests
        from django.http import HttpResponse

        try:
            message = request.POST.get("message")
            lang = request.POST.getlist("lang")
            #process text into chunks
            text = message.replace('\n','')
            text_list = re.split('(\,|\.)', text)
            combined_text = []
            for idx, val in enumerate(text_list):
                if idx % 2 == 0:
                    combined_text.append(val)
                else:
                    joined_text = ''.join((combined_text.pop(),val))
                    if len(joined_text) < 100:
                        combined_text.append(joined_text)
                    else:
                        subparts = re.split('( )', joined_text)
                        temp_string = ""
                        temp_array = []
                        for part in subparts:
                            temp_string = temp_string + part
                            if len(temp_string) > 80:
                                temp_array.append(temp_string)
                                temp_string = ""
                        #append final part
                        temp_array.append(temp_string)
                        combined_text.extend(temp_array)
            #download chunks and write them to the output file
            tmpsound = None
            for idx, val in enumerate(combined_text):
                headers = {"Host":"translate.google.com",
                  "Referer":"http://translate.google.com/",
                  "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36"}
                r = requests.get("http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (str(lang[0]), val, len(combined_text), idx),
                                 headers=headers)
                tmpsound += r.content
        except:
            pass
            #except FailedException as failure:
        #    return self.create_response(request, { 'status' : 'failure', 'reason' : failure }, HttpNotModified
        self.log_throttled_access(request)
        return HttpResponse(tmpsound, mimetype="audio/mpeg")

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