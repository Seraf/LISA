# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t; python-indent: 4 -*-
from pymongo import MongoClient
from lisa.server.service import configuration
from lisa.server.libs import LisaInstance

class IPlugin(object):
    """
    The most simple interface to be inherited when creating a plugin.
    """

    def __init__(self):
        """
        Set the basic variables.
        """
        self.lisa = LisaInstance
        self.configuration_lisa = configuration
        mongo = MongoClient(host=self.configuration_lisa['database']['server'],
                            port=self.configuration_lisa['database']['port'])
        self.is_activated = False
