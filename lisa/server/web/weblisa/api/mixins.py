from django.http import HttpResponse
 
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import convert_post_to_put

from ...interface.models import LisaUser
from tastypie.authentication import MultiAuthentication, ApiKeyAuthentication, SessionAuthentication


class PublicEndpointResourceMixin(object):
    """ Public endpoint dispatcher, for those routes upon which you don't want
        to enforce the current resources authentication limits."""
 
    def dispatch_public(self, request_type, request, **kwargs):
        """
            Same as `tastypie.resources.Resource.dispatch` except that
            we don't check if the user is authenticated
        """
        allowed_methods = getattr(self._meta, "%s_allowed_methods" % request_type, None)
 
        if 'HTTP_X_HTTP_METHOD_OVERRIDE' in request.META:
            request.method = request.META['HTTP_X_HTTP_METHOD_OVERRIDE']
 
        request_method = self.method_check(request, allowed=allowed_methods)
        method = getattr(self, "%s_%s" % (request_method, request_type), None)
 
        if method is None:
            raise ImmediateHttpResponse(response=http.HttpNotImplemented())
 
        self.throttle_check(request)
 
        # All clear. Process the request.
        request = convert_post_to_put(request)
        response = method(request, **kwargs)
 
        # Add the throttled request.
        self.log_throttled_access(request)
 
        # If what comes back isn't a ``HttpResponse``, assume that the
        # request was accepted and that some action occurred. This also
        # prevents Django from freaking out.
        if not isinstance(response, HttpResponse):
            return http.HttpNoContent()
 
        return response

class CustomApiKeyAuthentication(ApiKeyAuthentication):
    """
    Authenticates everyone if the request is GET otherwise performs
    ApiKeyAuthentication.
    """
    def is_mongouser_authenticated(self, request):
        """
        Custom solution for MongoUser ApiKey authentication.
        ApiKey here is not a class (as it is realized in ORM approach),
        but a field MongoUser class.
        """
        username, api_key = super(CustomApiKeyAuthentication,
                                  self).extract_credentials(request)
        try:
            User.objects.get(username=username, api_key=api_key)
        except:
            return False

        return True

    def is_authenticated(self, request, **kwargs):
        """
        Custom solution for `is_authenticated` function: MongoUsers has got
        authenticated through custom api_key check.
        """
        if request.method == 'GET':
            return True
        try:
            is_authenticated = super(CustomApiKeyAuthentication,
                                     self).is_authenticated(request, **kwargs)
        except TypeError as e:
            if "User" in str(e):
                is_authenticated = self.is_mongouser_authenticated(request)
            else:
                is_authenticated = False
        return is_authenticated