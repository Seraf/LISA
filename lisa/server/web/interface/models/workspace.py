from mongoengine import *
from mongoengine.django.auth import User

from lisa.server.web.weblisa.settings import DBNAME
connect(DBNAME)

class Workspace(DynamicDocument):
    class Meta:
        app_label = "interface"

    name = StringField(max_length=120, required=True, help_text='Name of the Workspace')
    widgets = ListField(ReferenceField('WidgetUser'), help_text="Contains a list of widgets")
    user = ReferenceField(User, required=True)
    meta = {
        'collection': 'workspaces',
        'allow_inheritance': False
    }