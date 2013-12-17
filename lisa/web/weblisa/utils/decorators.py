from django.http import Http404

class method_restricted_to(object):
    def __init__(self, methods=[]):
        self.methods = methods

    def __call__(self, f):
        def wrapped_f(request, *args):
            if request.method in self.methods:
                return f(request, *args)
            else:
                raise Http404
        return wrapped_f

class is_ajax(object):
    def __call__(self, f):
        def wrapped_f(request, *args):
            if request.is_ajax():
                return f(request, *args)
            else:
                raise Http404
        return wrapped_f