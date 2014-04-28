# -*- coding: UTF-8 -*-
import os, inspect
from pymongo import MongoClient
from lisa.server.service import configuration

import gettext

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
    inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
_ = translation = gettext.translation(domain='{{ plugin_name_lower }}', localedir=path, languages=[configuration['lang']]).ugettext

class {{ plugin_name }}:
    def __init__(self, lisa=None):
        self.lisa = lisa
        self.configuration_lisa = configuration
        self.mongo = MongoClient(self.configuration_lisa['database']['server'],
                            self.configuration_lisa['database']['port'])
        self.configuration = self.mongo.lisa.plugins.find_one({"name": "{{ plugin_name }}"})
        self.build_default_list()
        self.answer = None
        self.raw = None

