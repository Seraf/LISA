from zope.interface import implements

from twisted.python import usage
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin

from lisa.server import service

class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    
    tapname = "lisa-server"
    description = "Lisa server."
    
    def makeService(self):
        return service.makeService()

serviceMaker = ServiceMaker()
