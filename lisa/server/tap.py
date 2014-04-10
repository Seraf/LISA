# server/tap.py
from twisted.application import internet, service
from twisted.internet import interfaces
from twisted.python import usage
from lisa.server import service

def makeService(config):
    return service.makeService()
