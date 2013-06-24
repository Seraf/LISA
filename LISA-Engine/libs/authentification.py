from zope.interface import implements
from twisted.python import failure, log
from twisted.cred import portal, checkers, error, credentials
from twisted.internet import defer
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'web.lisa.settings'
from django.contrib.auth.models import User, check_password

class DjangoAuthChecker:
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,
                            credentials.IUsernameHashedPassword)

    def _passwordMatch(self, matched, user):
        if matched:
            return user
        else:
            return failure.Failure(error.UnauthorizedLogin())

    def requestAvatarId(self, credentials):
        try:
            user = User.objects.get(username=credentials.username)
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            return defer.maybeDeferred(
                check_password,
                credentials.password,
                user.password).addCallback(self._passwordMatch, user)
        except User.DoesNotExist:
            return defer.fail(error.UnauthorizedLogin())


class LISARealm(object):
    implements(portal.IRealm)

    def requestAvatar(self, user, mind):
        avatar = LISAAvatar(user)
        avatar.attached(mind)
        return avatar, lambda a=avatar:a.detached(mind)

class LISAAvatar():
    def __init__(self, user):
        self.user = user

    def attached(self, mind):
        self.remote = mind
        print 'User %s connected' % (self.user,)

    def detached(self, mind):
        self.remote = None
        print 'User %s disconnected' % (self.user,)