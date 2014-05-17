# -*- coding: UTF-8 -*-
import gettext
from pymongo import MongoClient
from twisted.python.reflect import namedAny
from twisted.python import log
from wit import Wit
import json

from lisa.server.ConfigManager import ConfigManagerSingleton

configuration = ConfigManagerSingleton.get().getConfiguration()
path = '/'.join([ConfigManagerSingleton.get().getPath(), 'lang'])
_ = translation = gettext.translation(domain='lisa', localedir=path, fallback=True,
                                              languages=[configuration['lang']]).ugettext


class RulesEngine():
    def __init__(self):
        client = MongoClient(configuration['database']['server'], configuration['database']['port'])
        self.database = client.lisa

        self.wit = Wit(configuration['wit_token'])

    def Rules(self, jsonData, lisaprotocol):
        rulescollection = self.database.rules
        intentscollection = self.database.intents
        if "outcome" in jsonData.keys():
            jsonInput = {}
            jsonInput['outcome'] = jsonData['outcome']
        else:
            jsonInput = self.wit.get_message(unicode(jsonData['body']))
        jsonInput['from'], jsonInput['type'], jsonInput['zone'] = jsonData['from'], jsonData['type'], jsonData['zone']

        if configuration['debug']['debug_before_before_rule']:
            log.msg(unicode(_("Before 'before' rule: %(jsonInput)s" % {'jsonInput': str(jsonInput)})))
        for rule in rulescollection.find({"enabled": True, "before": {"$ne":None}}).sort([("order", 1)]):
            exec(rule['before'])
        if configuration['debug']['debug_after_before_rule']:
            log.msg(unicode(_("After 'before' rule: %(jsonInput)s" % {'jsonInput': str(jsonInput)})))
        if configuration['debug']['debug_wit']:
            log.msg("WIT: " + str(jsonInput['outcome']))

        oIntent = intentscollection.find_one({"name": jsonInput['outcome']['intent']})
        if oIntent and jsonInput['outcome']['confidence'] >= configuration['wit_confidence']:
            instance = namedAny(str(oIntent["module"]))()
            methodToCall = getattr(instance, oIntent['function'])
            jsonOutput = methodToCall(jsonInput)
        else:
            jsonOutput = {}
            jsonOutput['plugin'] = "None"
            jsonOutput['method'] = "None"
            jsonOutput['body'] = _("I have not the right plugin installed to answer you correctly")
        jsonOutput['from'] = jsonData['from']
        if configuration['debug']['debug_before_after_rule']:
            log.msg(unicode(_("Before 'after' rule: %(jsonOutput)s" % {'jsonOutput': str(jsonOutput)})))
        for rule in rulescollection.find({"enabled": True, "after": {"$ne":None}}).sort([("order", 1)]):
            exec(rule['after'])
            #todo it doesn't check if the condition of the rule after has matched to end the rules
            if rule['end']:
                break
        if configuration['debug']['debug_after_after_rule']:
            log.msg(unicode(_("After 'after' rule: %(jsonOutput)s" % {'jsonOutput': str(jsonOutput)})))
