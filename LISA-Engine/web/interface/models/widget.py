from mongoengine import *
from mongoengine.django.auth import User
from web.interface.models.workspace import Workspace

try:
    from web.lisa.settings import DBNAME
except ImportError:
    from lisa.settings import DBNAME
connect(DBNAME)

class Widget(DynamicDocument):
    class Meta:
        app_label = "interface"

    name = StringField(required=True, help_text="Widget name")
    view = StringField(required=True, help_text="View of the plugin")
    meta = {
        'collection': 'widgets',
        'allow_inheritance': False
    }

class WidgetUser(DynamicDocument):
    class Meta:
        app_label = "interface"

    workspace = ReferenceField(Workspace, reverse_workspacedelete_rule=CASCADE)
    coordx = IntField(required=True, help_text="X coord")
    coordy = IntField(required=True, help_text="X coord")
    user = ReferenceField(User, reverse_userdelete_rule=CASCADE)
    meta = {
        'collection': 'widgets_users',
        'allow_inheritance': False
    }