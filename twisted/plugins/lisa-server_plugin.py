from zope.interface import implements

from twisted.python import usage
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin

from lisaserver import lisa

class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    
    tapname = "lisa-server"
    description = "Lisa server."
    
    def makeService(self):
        return lisa.makeService()

serviceMaker = ServiceMaker()
