from mongoengine import *
from mongoengine.django.auth import User
try:
    from web.lisa.settings import DBNAME
except ImportError:
    from lisa.settings import DBNAME
connect(DBNAME)

class Workspace(DynamicDocument):
    name = StringField(max_length=120, required=True, help_text='Name of the Workspace')
    widgets = ListField(EmbeddedDocumentField(Widget), help_text="Contains a list of widgets")
    user = ReferenceField(User)
    meta = {
        'collection': 'plugins',
        'allow_inheritance': False
    }


class Widget(DynamicDocument):
    workspace = ReferenceField(Workspace, reverse_dashboarddelete_rule=CASCADE)
    coordx = IntField(required=True, help_text="X coord")
    coordy = IntField(required=True, help_text="X coord")
    view = StringField(required=True, help_text="View of the plugin")
    enabled = BooleanField()
    meta = {
        'collection': 'rules',
        'allow_inheritance': False
    }