from django.http import HttpResponse
 
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import convert_post_to_put
 
 
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