from twisted.python import log
from tastypie import authorization
from django.conf.urls import *
import json, os
from lisa.server.libs import LisaFactorySingleton, LisaProtocolSingleton, configuration
from tastypie import resources as tastyresources
from tastypie_mongoengine import resources as mongoresources
from tastypie.utils import trailing_slash
from mongoengine.django.auth import User
from wit import Wit
from lisa.server.web.weblisa.settings import LISA_PATH

class UserResource(mongoresources.MongoEngineResource):
    class Meta:
        resource_name = 'user'
        allowed_methods = ('get','post')
        authorization = authorization.Authorization()
        object_class = User

class Lisa(object):
    def __init__(self):
        return None

class LisaResource(tastyresources.Resource):
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
                'name': 'intents',
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
            },
            {
                'name': 'tts/pico',
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

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/engine/reload%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('engine_reload'), name="api_lisa_engine_reload"),
            url(r"^(?P<resource_name>%s)/scheduler/reload%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('scheduler_reload'), name="api_lisa_scheduler_reload"),
            url(r"^(?P<resource_name>%s)/tts/google%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('tts_google'), name="api_lisa_tts_google"),
            url(r"^(?P<resource_name>%s)/tts/pico%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('tts_pico'), name="api_lisa_tts_pico"),
            url(r"^(?P<resource_name>%s)/speak%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('speak'), name="api_lisa_speak"),
            url(r"^(?P<resource_name>%s)/intents%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('intents'), name="api_lisa_intents"),
        ]

    def speak(self, request, **kwargs):
        self.method_check(request, allowed=['post', 'get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        if request.POST:
            message = request.POST.get("message")
            clients_zone = request.POST.getlist("clients_zone")
        else:
            message = request.GET.get("message")
            clients_zone = request.GET.getlist("clients_zone")
        jsondata = json.dumps({
                                      'body': message,
                                      'clients_zone': clients_zone,
                                      'from': "API",
                                      'type': "chat"
            })
        LisaProtocolSingleton.get().answerToClient(jsondata=jsondata)

        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'log': "Message sent"}, HttpAccepted)

    def tts_google(self, request, **kwargs):
        self.method_check(request, allowed=['post', 'get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified
        import re
        import requests
        from django.http import HttpResponse
        combined_sound = []
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
            for idx, val in enumerate(combined_text):
                headers = {"Host":"translate.google.com",
                           "Referer":"http://translate.google.com/",
                           "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36"}
                r = requests.get("http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (str(lang[0]), val, len(combined_text), idx),
                                 headers=headers)

                combined_sound.append(r.content)
        except:
            log.err()
            return self.create_response(request, { 'status' : 'failure' }, HttpNotModified)
        self.log_throttled_access(request)
        return HttpResponse(''.join(combined_sound), content_type="audio/mpeg", mimetype="audio/mpeg")

    def tts_pico(self, request, **kwargs):
        import uuid
        self.method_check(request, allowed=['post', 'get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        message = request.POST.get("message")
        lang = request.POST.getlist("lang")


        from tastypie.http import HttpAccepted, HttpNotModified
        from django.http import HttpResponse
        from subprocess import call, Popen
        combined_sound = []
        temp = LISA_PATH + "/tmp/" + str(uuid.uuid4()) + ".wav"
        language = str(lang[0])+'-'+str(lang[0]).upper()
        command = ['pico2wave', '-w', temp, '-l', language, '--', message]
        try:
            call(command)
            #combined_sound.append(content)
        except OSError:
            log.err()
            return self.create_response(request, { 'status' : 'failure' }, HttpNotModified)
        f = open(temp,"rb")
        combined_sound.append(f.read())
        f.close()
        os.remove(temp)
        self.log_throttled_access(request)
        return HttpResponse(''.join(combined_sound), content_type="audio/mpeg", mimetype="audio/mpeg")

    def engine_reload(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            LisaFactorySingleton.get().LisaReload()
        except:
            log.err()
            return self.create_response(request, { 'status' : 'failure' }, HttpNotModified)
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'log': "L.I.S.A Engine reloaded"}, HttpAccepted)

    def intents(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.wit = Wit(self.configuration['wit_token'])

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            intents = self.wit.get_intents()
        except:
            log.err()
            return self.create_response(request, { 'status' : 'failure' }, HttpNotModified)
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'intents': intents}, HttpAccepted)

    def scheduler_reload(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        try:
            LisaFactorySingleton.get().SchedReload()
        except:
            log.err()
            return self.create_response(request, { 'status' : 'failure' }, HttpNotModified)
        self.log_throttled_access(request)
        return self.create_response(request, { 'status': 'success', 'log': "L.I.S.A Task Scheduler reloaded"},
                                    HttpAccepted)

    def get_object_list(self, request):
        return [Lisa()]