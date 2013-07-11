from mongoengine import *
from mongoengine.django.auth import User

try:
    from web.lisa.settings import DBNAME
except ImportError:
    from lisa.settings import DBNAME
connect(DBNAME)

class Workspace(DynamicDocument):
    class Meta:
        app_label = "interface"

    name = StringField(max_length=120, required=True, help_text='Name of the Workspace')
    widgets = ListField(EmbeddedDocumentField('WidgetUser'), help_text="Contains a list of widgets")
    user = ReferenceField(User)
    meta = {
        'collection': 'workspaces',
        'allow_inheritance': False
    }