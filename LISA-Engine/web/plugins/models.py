from mongoengine import *
from web.lisa.settings import DBNAME
connect(DBNAME)


class Plugin(DynamicDocument):
    name = StringField(max_length=120, required=True)
    lang = ListField(StringField(max_length=2))
    enabled = BooleanField()
    version = FloatField()
    configuration = DictField()
    meta = {
        'collection': 'plugins',
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