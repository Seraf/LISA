from mongoengine import *
from web.jarvis.settings import DBNAME
connect(DBNAME)


class Plugin(DynamicDocument):
    name = StringField(max_length=120, required=True)
    lang = ListField(StringField(max_length=2))
    meta = {
        'collection': 'plugins',
        'allow_inheritance': False
    }
