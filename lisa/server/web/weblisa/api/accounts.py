from ...interface.models import LisaUser
from django.contrib.auth import login, logout
from mongoengine.queryset import DoesNotExist
from tastypie_mongoengine import resources as mongoresources
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpAccepted
from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.authentication import MultiAuthentication
from django.conf.urls import *
from .mixins import PublicEndpointResourceMixin, CustomApiKeyAuthentication
from tastypie import authorization
from mongoengine import document

class ProfileResource(mongoresources.MongoEngineResource):

    class Meta:
        queryset = LisaUser.objects.all()
        authentication = MultiAuthentication(CustomApiKeyAuthentication())
        allowed_methods = ['get', ]
        resource_name = 'profile'


class UserResource(PublicEndpointResourceMixin, mongoresources.MongoEngineResource):
    features = fields.DictField(blank=True, null=True, readonly=True)
    apikey = fields.CharField(blank=True, null=True, readonly=True)
    user_permissions = fields.ListField(blank=True, null=True, readonly=True)

    class Meta:
        queryset = LisaUser.objects.all()
        authentication = MultiAuthentication(CustomApiKeyAuthentication())
        authorization = authorization.Authorization()

        """fields = ['username', 'first_name', 'last_name', 'apikey',
                  'api_key_created', 'email', 'date_joined',
                  'is_active', 'is_superuser', 'is_staff', 'id',
                  'features', 'user_permissions'
        ]"""

        # FIXME :Problem with the put : why I receive an _id field on mongodb save with user and not plugin ?
        allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        login_allowed_methods = ['post', ]
        extra_actions = [
            {
                'name': 'login',
                'http_method': 'POST',
                'resource_type': 'list',
                'fields': {
                    'username': {
                        'type': 'string',
                        'required': True,
                        'description': 'Unique username required.'
                    },
                    'password': {
                        'type': 'string',
                        'required': True,
                        'description': 'password required'
                    }
                }
            },
            {
                'name': 'logout',
                'http_method': 'POST',
                'resource_type': 'list',
                'fields': {}
            },
            {
                'name': 'regenerateapikey',
                'summary': 'Regenerate the API Key for a user',
                'http_method': 'GET',
                'fields': {}
            }

        ]

    def dehydrate_user_permissions(self, bundle):
        user = bundle.obj
        #user_app_permissions = user.user_permissions.all()
        #user_object_permissions = UserObjectPermission.objects.filter(user=user).distinct()
        #return list(user_app_permissions.values_list('codename', flat=True)) + list(user_object_permissions.values_list('permission__codename', flat=True))

    def dehydrate_apikey(self, bundle):
        user = bundle.obj
        if hasattr(user, 'api_key') and user.api_key:
            return user.api_key

        return None

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/regenerateapikey%s" % (self._meta.resource_name,
                                                                                  trailing_slash()),
                self.wrap_view('regenerate_api_key'), name='api_user_regenerate_api_key'),
            url(r"^(?P<resource_name>%s)/login%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_login'), name='api_user_login'),
            url(r"^(?P<resource_name>%s)/logout%s" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_logout'), name='api_user_logout'),

        ]

    def regenerate_api_key(self, request, **kwargs):
        self.method_check(request, allowed=['post', 'get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        queryset = LisaUser.objects(pk=kwargs['pk'])
        for user in queryset:
            user.apikey = user.set_api_key()
            user.save()
        status = {'username': user.username, 'apikey': user.apikey}
        self.log_throttled_access(request)
        return self.create_response(request, status, HttpAccepted)


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

        try:
            user = LisaUser.objects.get(username=username)
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            if user.check_password(password):
                login(request, user)
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
