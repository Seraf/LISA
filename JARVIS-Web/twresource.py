from twisted.web import server, resource, client
from twisted.internet import defer


class Root(resource.Resource):

    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource


class GoogleResource(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)

    def getChild(self, name, request):
        return self

    @defer.inlineCallbacks
    def get_page(self, request, q):
        page = yield client.getPage("http://google.com/search?q=%s" % q)
        request.write(page)
        request.finish()

    def render_GET(self, request):
        q = request.args.get('q', [""])[0]
        self.get_page(request, q)
        return server.NOT_DONE_YET


