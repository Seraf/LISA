from mongoengine import *
from mongoengine.django.auth import User

from lisa.server.web.weblisa.settings import DBNAME
connect(DBNAME)

class Widget(DynamicDocument):
    class Meta:
        app_label = "interface"

    name = StringField(required=True, help_text="Widget name")
    plugin = ReferenceField('Plugin', required=True)
    view = StringField(required=True, help_text="View of the plugin")
    meta = {
        'collection': 'widgets',
        'allow_inheritance': False
    }

class WidgetUser(DynamicDocument):
    class Meta:
        app_label = "interface"

    coordx = IntField(required=True, help_text="X coord")
    coordy = IntField(required=True, help_text="X coord")
    user = ReferenceField(User, required=True)
    widget = ReferenceField('Widget', required=True)
    meta = {
        'collection': 'widgets_users',
        'allow_inheritance': False
    }