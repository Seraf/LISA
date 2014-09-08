from twisted.python import log
from tastypie import authorization
from django.conf.urls import *
import json, os
from ....libs import LisaFactorySingleton, LisaProtocolSingleton
from ....ConfigManager import ConfigManagerSingleton
from tastypie import resources as tastyresources
from tastypie.utils import trailing_slash
from wit import Wit

configuration = ConfigManagerSingleton.get().getConfiguration()
dir_path = ConfigManagerSingleton.get().getPath()

from .mixins import CustomApiKeyAuthentication
from tastypie.authentication import MultiAuthentication, SessionAuthentication


class Lisa(object):
    def __init__(self):
        return None

class LisaResource(tastyresources.Resource):
    class Meta:
        resource_name = 'lisa'
        allowed_methods = ()
        authorization = authorization.Authorization()
        object_class = Lisa
        authentication = MultiAuthentication(CustomApiKeyAuthentication())
        extra_actions = [
            {
                'name': 'configuration',
                'http_method': 'GET',
                'resource_type': 'list',
                'fields': {}
            },
            {
                'name': 'version',
                'http_method': 'GET',
                'resource_type': 'list',
                'fields': {}
            },
            {
                'name': 'engine/reload',
                'http_method': 'GET',
                'resource_type': 'list',
                'fields': {}
            },
            {
                'name': 'scheduler/reload',
                'http_method': 'GET',
                'resource_type': 'list',
                'fields': {}
            },
            {
                'name': 'witintents',
                'http_method': 'GET',
                'resource_type': 'list',
                'fields': {}
            },
            {
                'name': 'speak',
                'http_method': 'POST',
                'resource_type': 'list',
                'fields': {
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
                'name': 'tts-google',
                'http_method': 'POST',
                'resource_type': 'list',
                'fields': {
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
                'name': 'tts-pico',
                'http_method': 'POST',
                'resource_type': 'list',
                'fields': {
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
            url(r"^(?P<resource_name>%s)/configuration%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('configuration'), name="api_lisa_configuration"),
            url(r"^(?P<resource_name>%s)/version%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('version'), name="api_lisa_version"),
            url(r"^(?P<resource_name>%s)/engine/reload%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('engine_reload'), name="api_lisa_engine_reload"),
            url(r"^(?P<resource_name>%s)/scheduler/reload%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('scheduler_reload'), name="api_lisa_scheduler_reload"),
            url(r"^(?P<resource_name>%s)/tts-google%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('tts_google'), name="api_lisa_tts_google"),
            url(r"^(?P<resource_name>%s)/tts-pico%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('tts_pico'), name="api_lisa_tts_pico"),
            url(r"^(?P<resource_name>%s)/speak%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('speak'), name="api_lisa_speak"),
            url(r"^(?P<resource_name>%s)/witintents%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('witintents'), name="api_lisa_witintents"),
        ]

    def speak(self, request, **kwargs):
        self.method_check(request, allowed=['post', 'get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        if request.method == 'POST':
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
        return self.create_response(request, {'status': 'success', 'log': "Message sent"}, HttpAccepted)

    def tts_google(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified
        import re
        import requests
        from django.http import HttpResponse
        combined_sound = []
        try:
            if request.method == 'POST':
                message = request.POST.get("message")
                lang = request.POST.get("lang")
                if not message:
                    # In case there isn't form data, let's check the body
                    post = json.loads(request.body)
                    message = post['message']
                    lang = post['lang']
            #process text into chunks
            text = message.replace('\n', '')
            text_list = re.split('(\.)', text)
            combined_text = []
            for idx, val in enumerate(text_list):
                if idx % 2 == 0:
                    combined_text.append(val)
                else:
                    joined_text = ''.join((combined_text.pop(), val))
                    if len(joined_text) < 100:
                        combined_text.append(joined_text)
                    else:
                        subparts = re.split('( )', joined_text)
                        temp_string = ""
                        temp_array = []
                        for part in subparts:
                            temp_string += part
                            if len(temp_string) > 80:
                                temp_array.append(temp_string)
                                temp_string = ""
                            #append final part
                        temp_array.append(temp_string)
                        combined_text.extend(temp_array)
                #download chunks and write them to the output file
            for idx, val in enumerate(combined_text):
                headers = {"Host": "translate.google.com",
                           "Referer": "https://translate.google.com/",
                           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36"}
                r = requests.get("https://translate.google.com/translate_tts?ie=UTF-8&tl=%s&q=%s&total=%s&idx=%s&client=t&prev=input" % (
                    lang, val, len(combined_text), idx), headers=headers)
                combined_sound.append(r.content)
        except:
            log.err()
            return self.create_response(request, {'status': 'failure'}, HttpNotModified)
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
        temp = dir_path + "/tmp/" + str(uuid.uuid4()) + ".wav"
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

    def witintents(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.wit = Wit(configuration['wit_token'])

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
        return self.create_response(request, {'status': 'success', 'log': 'L.I.S.A Task Scheduler reloaded'},
                                    HttpAccepted)

    def configuration(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        from tastypie.http import HttpAccepted, HttpNotModified

        self.log_throttled_access(request)
        copyconfiguration = configuration
        copyconfiguration['database'] = None
        return self.create_response(request, {'configuration': configuration}, HttpAccepted)

    def version(self, request, **kwargs):
        from tastypie.http import HttpAccepted, HttpNotModified
        from pkg_resources import get_distribution
        import requests

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)

        local_version = get_distribution('lisa-server').version
        should_upgrade = False

        r = requests.get('https://pypi.python.org/pypi/lisa-server/json')
        if r.status_code == requests.codes.ok:
            remote_version = r.json()['info']['version']
            
        else:
            return self.create_response(request, {'status': 'fail', 'log': 'Problem contacting pypi.python.org'}, HttpAccepted)

        if remote_version > local_version:
            should_upgrade = True

        response = {
            'local_version': get_distribution('lisa-server').version,
            'remote_version': remote_version,
            'should_upgrade': should_upgrade
        }

        return self.create_response(request, response, HttpAccepted)

    def get_object_list(self, request):
        return [Lisa()]