import sys
from twisted.web import resource

class Root(resource.Resource):
    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource

class LisaReload(resource.Resource):
    def __init__(self, LisaFactory):
        self.LisaFactory = LisaFactory
        sys.path = self.LisaFactory.syspath
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        self.LisaFactory.build_grammar()
        return "OK"

    def render_GET(self, request):
        self.LisaFactory.build_grammar()
        return "OK"

class Scheduler_reload(resource.Resource):
    def __init__(self, taskman):
        self.taskman = taskman
        resource.Resource.__init__(self)
    def getChild(self, path, request):
        return self.taskman.reload()

    def render_GET(self, request):
        return self.taskman.reload()

def verifyCallback(connection, x509, errnum, errdepth, ok):
    if not ok:
        print 'invalid cert from subject:', x509.get_subject()
        return False
    else:
        print "Certs are OK"
    return True

