# -*- coding: UTF-8 -*-
import json, os
from pymongo import MongoClient
from wit import Wit
from lisa.server.web.manageplugins.models import Intent as oIntents
import gettext
import lisa.server

from lisa.server.ConfigManager import ConfigManagerSingleton

configuration = ConfigManagerSingleton.get().getConfiguration()
path = '/'.join([ConfigManagerSingleton.get().getPath(), 'lang'])
_ = translation = gettext.translation(domain='intents', localedir=path, fallback=True,
                                              languages=[configuration['lang']]).ugettext

class Intents:
    def __init__(self, lisa=None):
        self.lisa = lisa
        self.configuration = configuration
        mongo = MongoClient(host=self.configuration['database']['server'],
                            port=self.configuration['database']['port'])
        self.database = mongo.lisa
        self.wit = Wit(self.configuration['wit_token'])

    def list(self, jsonInput):
        intentstr = []
        listintents = self.wit.get_intents()
        for oIntent in oIntents.objects(enabled=True):
            for witintent in listintents:
                print witintent
                if witintent["name"] == oIntent.name and 'metadata' in witintent:
                    if witintent['metadata']:
                        metadata = json.loads(witintent['metadata'])
                        intentstr.append(metadata['tts'])

        return {"plugin": "Intents",
                "method": "list",
                "body": unicode(_('I can %(intentslist)s' % {'intentslist': ', '.join(intentstr)}))
        }
