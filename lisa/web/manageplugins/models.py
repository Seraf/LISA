from mongoengine import *
try:
    from web.lisa.settings import DBNAME
except ImportError:
    from lisa.settings import DBNAME
connect(DBNAME)

class Description(EmbeddedDocument):
    lang = StringField(max_length=2)
    description = StringField()

class Plugin(DynamicDocument):
    name = StringField(max_length=120, required=True, help_text='Name of the plugin')
    lang = ListField(StringField(max_length=2), help_text="List of supported languages : ['all','WebSocket']")
    enabled = BooleanField(help_text="Boolean to know if the plugin is enabled or not")
    version = StringField(help_text="The version number of the plugin")
    description = ListField(EmbeddedDocumentField(Description), help_text="Contains a description of the plugin")
    configuration = DictField(help_text="Configuration dictionnary of the plugin")
    meta = {
        'collection': 'plugins',
        'allow_inheritance': False
    }

class Intents(DynamicDocument):
    plugin = ReferenceField(Plugin, reverse_delete_rule=CASCADE)
    name = StringField()
    meta = {
        'collection': 'intents',
        'allow_inheritance': False
    }

class Rule(DynamicDocument):
    plugin = ReferenceField(Plugin, reverse_delete_rule=CASCADE)
    enabled = BooleanField()
    meta = {
        'collection': 'rules',
        'allow_inheritance': False
    }
class Cron(DynamicDocument):
    plugin = ReferenceField(Plugin, reverse_delete_rule=CASCADE)
    enabled = BooleanField()
    meta = {
        'collection': 'crons',
        'allow_inheritance': False
    }