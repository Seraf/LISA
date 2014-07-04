from ...interface.user import User
from django.contrib.auth import login, logout, authenticate
from mongoengine.queryset import DoesNotExist
from django.db.models import Q
from tastypie_mongoengine import resources as mongoresources
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.authentication import MultiAuthentication, SessionAuthentication
from django.conf.urls import *
from waffle import sample_is_active
from waffle.models import Flag, Switch, Sample
from guardian.models import UserObjectPermission

import uuid
import hashlib
import hmac
import datetime

from .authorizations import UserOnlyAuthorization
from .mixins import PublicEndpointResourceMixin, CustomApiKeyAuthentication


class ProfileResource(mongoresources.MongoEngineResource):

    class Meta:
        queryset = User.objects.all()
        authentication = MultiAuthentication(CustomApiKeyAuthentication(), SessionAuthentication())
        allowed_methods = ['get', ]
        resource_name = 'profile'


class UserResource(PublicEndpointResourceMixin, mongoresources.MongoEngineResource):
    features = fields.DictField(blank=True, null=True, readonly=True)
    apikey = fields.CharField(blank=True, null=True, readonly=True)
    user_permissions = fields.ListField(blank=True, null=True, readonly=True)

    class Meta:
        queryset = User.objects.all()
        authentication = MultiAuthentication(CustomApiKeyAuthentication(), SessionAuthentication())
        #authorization = UserOnlyAuthorization()
        fields = ['pk', 'username', 'first_name', 'last_name', 'email', ]
        allowed_methods = ['get', 'post']
        login_allowed_methods = ['post', ]
        resource_name = 'user'
        extra_actions = [
            {
                'name': 'login',
                'http_method': 'POST',
                'fields': {}
            },
            {
                'name': 'logout',
                'http_method': 'POST',
                'fields': {}
            },
        ]

    def dehydrate_user_permissions(self, bundle):
        user = bundle.obj
        user_app_permissions = user.user_permissions.all()
        user_object_permissions = UserObjectPermission.objects.filter(user=user).distinct()
        return list(user_app_permissions.values_list('codename', flat=True)) + list(user_object_permissions.values_list('permission__codename', flat=True))

    def dehydrate_features(self, bundle):
        user = bundle.obj
        users_groups = user.groups.all()

        find_everyone_flags = Q(everyone=True)
        find_rollout_flags = Q(rollout=True)
        find_authenticated_flags = Q(authenticated=True)
        find_user_flags = Q(users__in=[user.id])
        find_group_flags = Q(groups__in=users_groups)

        enabled_flags = Flag.objects.filter(find_everyone_flags | find_rollout_flags | find_authenticated_flags | find_user_flags | find_group_flags)
        enabled_switches = Switch.objects.filter(active=True)
        enabled_samples = []
        for sample in Sample.objects.all():
            if sample_is_active(sample):
                enabled_samples.append(sample.name)

        flags = list(set(enabled_flags.values_list('name', flat=True)))
        switches = list(set(enabled_switches.values_list('name', flat=True)))
        samples = list(set(enabled_samples))
        return {
            "flags": flags,
            "switches": switches,
            "samples": samples,
            "all": " ".join(flags + switches + samples)
        }

    def dehydrate_apikey(self, bundle):
        user = bundle.obj
        if hasattr(user, 'api_key') and user.api_key.key:
            return user.api_key.key

        return None

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_login'), name='api_user_login'),
            url(r"^(?P<resource_name>%s)/logout%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('dispatch_logout'), name='api_user_logout'),
        ]

    def dispatch_login(self, request, **kwargs):
        """
        A view for handling the various HTTP methods (GET/POST/PUT/DELETE) on
        a single resource.

        Relies on ``Resource.dispatch`` for the heavy-lifting.
        """
        return self.dispatch_public('login', request, **kwargs)

    def post_login(self, request, **kwargs):
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        username = data.get('username', '')
        password = data.get('password', '')
        from twisted.python import log

        log.msg("===============")
        for user in User.objects.all():
            log.msg("debug: %s" % user)
        log.msg("===============")
        log.msg(username)
        log.msg(password)


        try:
            user = User.objects.get(username=username)
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            log.msg(user)
            if user.check_password(password):
                print login(request, user)
                request.session.set_expiry(60 * 60 * 1)  # 1 hour timeout
                return self.get_detail(request, pk=user.id)
            else:
                return self.create_response(request, {'success': False, 'reason': 'disabled', }, HttpForbidden)
        except DoesNotExist:
            return self.create_response(request, {'success': False, 'reason': 'incorrect'}, HttpUnauthorized)


    def dispatch_logout(self, request, **kwargs):
        """
        A view for handling the various HTTP methods (GET/POST/PUT/DELETE) on
        a single resource.

        Relies on ``Resource.dispatch`` for the heavy-lifting.
        """
        return self.dispatch('logout', request, **kwargs)

    def get_logout(self, request, **kwargs):
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            # Not logged in
            return self.create_response(request, {'success': False}, HttpUnauthorized)


EnabledResources = (
    UserResource,
    ProfileResource
)
