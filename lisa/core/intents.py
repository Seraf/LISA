# -*- coding: UTF-8 -*-
from datetime import datetime
import json, os, inspect
from pymongo import MongoClient
from lisa import configuration
from libs import Wit
from web.manageplugins.models import Intents as oIntents

import gettext

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("lang"))))
_ = translation = gettext.translation(domain='intents', localedir=path, languages=[configuration['lang']]).ugettext

class Intents:
    def __init__(self, lisa=None):
        self.lisa = lisa
        self.configuration = configuration
        mongo = MongoClient(host=self.configuration['database']['server'],
                            port=self.configuration['database']['port'])

    def list(self, jsonInput):
        oWit = Wit(self.configuration)
        listintents = oWit.list_intents()
        for intent in oIntents.objects.all():
            print intent
        return {"plugin": "Intents",
                "method": "list",
                "body": str(listintents)
        }
