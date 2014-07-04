from mongoengine.django.auth import User as BaseUser
from tastypie import fields
import hashlib
import datetime
import hmac
import uuid


class User(BaseUser):
    """
    Subclass of mongoengine.django.auth.User with API key for authentication.
    """
    print "=========================here================================="
    api_key = fields.CharField(default='')
    api_key_created = fields.DateTimeField(help_text='Created')

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.set_api_key()

        return super(User, self).save(*args, **kwargs)

    def set_api_key(self):
        self.api_key = self.generate_key()
        self.api_key_created = datetime.datetime.now()

    def generate_key(self):
        new_uuid = uuid.uuid4()
        return hmac.new(str(new_uuid), digestmod=hashlib.sha1).hexdigest()

from mongoengine import signals
from tastypie.models import create_api_key
signals.post_save.connect(create_api_key, sender=User)