# -*- coding: UTF-8 -*-
import os
from twisted.internet import reactor, ssl
from twisted.application import internet, service
from twisted.web import server, wsgi, static
from twisted.python import threadpool, log
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.resource import WebSocketResource
from OpenSSL import SSL
from lisa.server.ConfigManager import ConfigManagerSingleton

class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()


# Twisted Application Framework setup:
application = service.Application('LISA')

def makeService(config):
    from django.core.handlers.wsgi import WSGIHandler
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lisa.server.web.weblisa.settings'


    if config['configuration']:
        ConfigManagerSingleton.get().setConfiguration(config['configuration'])

    configuration = ConfigManagerSingleton.get().getConfiguration()
    dir_path = ConfigManagerSingleton.get().getPath()

    from lisa.server import libs

    # Creating MultiService
    multi = service.MultiService()
    pool = threadpool.ThreadPool()
    tps = ThreadPoolService(pool)
    tps.setServiceParent(multi)

    # Creating the web stuff
    resource_wsgi = wsgi.WSGIResource(reactor, tps.pool, WSGIHandler())
    root = libs.Root(resource_wsgi)
    staticrsrc = static.File('/'.join([dir_path,'web/interface/static']))
    root.putChild("static", staticrsrc)

    # Create the websocket
    if configuration['enable_secure_mode']:
        socketfactory = WebSocketServerFactory("wss://" + configuration['lisa_url'] + ":" +
                                               str(configuration['lisa_web_port_ssl']),debug=False)
    else:
        socketfactory = WebSocketServerFactory("ws://" + configuration['lisa_url'] + ":" +
                                               str(configuration['lisa_web_port']),debug=False)
    socketfactory.protocol = libs.WebSocketProtocol
    socketfactory.protocol.configuration, socketfactory.protocol.dir_path = configuration, dir_path
    socketresource = WebSocketResource(socketfactory)
    root.putChild("websocket", socketresource)

    # Configuring servers to launch
    if configuration['enable_secure_mode'] or configuration['enable_unsecure_mode']:
        if configuration['enable_secure_mode']:
            SSLContextFactoryEngine = ssl.DefaultOpenSSLContextFactory(
                os.path.normpath(dir_path + '/' + 'configuration/ssl/server.key'),
                os.path.normpath(dir_path + '/' + 'configuration/ssl/server.crt')
            )
            SSLContextFactoryWeb = ssl.DefaultOpenSSLContextFactory(
                os.path.normpath(dir_path + '/' + 'configuration/ssl/server.key'),
                os.path.normpath(dir_path + '/' + 'configuration/ssl/server.crt')
            )
            ctx = SSLContextFactoryEngine.getContext()
            ctx.set_verify(
                SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT,
                libs.verifyCallback
            )
            # Since we have self-signed certs we have to explicitly
            # tell the server to trust them.
            with open(os.path.normpath(dir_path + '/' + 'configuration/ssl/server.pem'), 'w') as outfile:
                for file in os.listdir(os.path.normpath(dir_path + '/' + 'configuration/ssl/public/')):
                    with open(os.path.normpath(dir_path + '/' + 'configuration/ssl/public/'+file)) as infile:
                        for line in infile:
                            outfile.write(line)


            ctx.load_verify_locations(os.path.normpath(dir_path + '/' + 'configuration/ssl/server.pem'))
            internet.SSLServer(configuration['lisa_web_port_ssl'],
                               server.Site(root), SSLContextFactoryWeb).setServiceParent(multi)
            internet.SSLServer(configuration['lisa_engine_port_ssl'],
                               libs.LisaFactorySingleton.get(), SSLContextFactoryEngine).setServiceParent(multi)
        if configuration['enable_unsecure_mode']:
            # Serve it up:
            internet.TCPServer(configuration['lisa_web_port'], server.Site(root)).setServiceParent(multi)
            internet.TCPServer(configuration['lisa_engine_port'], libs.LisaFactorySingleton.get()).setServiceParent(multi)

    else:
        exit(1)
    libs.scheduler.setServiceParent(multi)
    multi.setServiceParent(application)
    libs.Initialize()
    return multi
