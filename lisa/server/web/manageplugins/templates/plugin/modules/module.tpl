# -*- coding: UTF-8 -*-
from lisa.server.plugins.IPlugin import IPlugin
import gettext
import inspect
import os

class {{ plugin_name }}(IPlugin):
    def __init__(self):
        super({{ plugin_name }}, self).__init__()
        self.configuration_plugin = self.mongo.lisa.plugins.find_one({"name": "{{ plugin_name }}"})
        self.path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(
            inspect.getfile(inspect.currentframe()))[0],os.path.normpath("../lang/"))))
        self._ = translation = gettext.translation(domain='{{ plugin_name_lower }}',
                                                   localedir=self.path,
                                                   fallback=True,
                                                   languages=[self.configuration_lisa['lang']]).ugettext

    def sayHello(self, jsonInput):
        return {"plugin": "{{ plugin_name }}",
                "method": "sayHello",
                "body": self._('Hello. How are you ?')
        }
