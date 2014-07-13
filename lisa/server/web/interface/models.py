from mongoengine.django.auth import User as BaseUser
from tastypie import fields
from mongoengine import *
import hashlib
import datetime
import hmac
import uuid

from mongoengine import *

from lisa.server.web.weblisa.settings import DBNAME
connect(DBNAME)

class LisaUser(BaseUser):
    """
    Subclass of mongoengine.django.auth.User with API key for authentication.
    """
    class Meta:
        app_label = 'interface'

    api_key = StringField(default='')
    api_key_created = DateTimeField(help_text='Created')

    def save(self, *args, **kwargs):
        if not self.api_key:
            print "not self apikey :("
            self.set_api_key()

        return super(LisaUser, self).save(*args, **kwargs)

    def set_api_key(self):
        self.api_key = self.generate_key()
        self.api_key_created = datetime.datetime.now()

    def generate_key(self):
        new_uuid = uuid.uuid4()
        return hmac.new(str(new_uuid), digestmod=hashlib.sha1).hexdigest()

#from mongoengine import signals
#from tastypie.models import create_api_key
#signals.post_save.connect(create_api_key, sender=LisaUser)


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
    user = ReferenceField(LisaUser, required=True)
    widget = ReferenceField('Widget', required=True)
    meta = {
        'collection': 'widgets_users',
        'allow_inheritance': False
    }


class Workspace(DynamicDocument):
    class Meta:
        app_label = "interface"

    name = StringField(max_length=120, required=True, help_text='Name of the Workspace')
    widgets = ListField(ReferenceField('WidgetUser'), help_text="Contains a list of widgets")
    user = ReferenceField(LisaUser, required=True)
    meta = {
        'collection': 'workspaces',
        'allow_inheritance': False
    }