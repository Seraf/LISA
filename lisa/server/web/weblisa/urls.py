from django.conf.urls import patterns, include, url
from tastypie.api import Api
from lisa.server.web.manageplugins.api import PluginResource, IntentResource
from lisa.server.web.interface.api import WidgetResource, WorkspaceResource, WidgetByUserResource
from api import LisaResource, UserResource
from twisted.python.reflect import namedAny
import tastypie_swagger

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(PluginResource())
v1_api.register(IntentResource())
v1_api.register(WorkspaceResource())
v1_api.register(WidgetResource())
v1_api.register(WidgetByUserResource())
v1_api.register(LisaResource())

urlpatterns = patterns('',
    url(r'^speech/', include('lisa.server.web.googlespeech.urls')),
    url(r'^plugins/', include('lisa.server.web.manageplugins.urls')),
    url(r'', include('lisa.server.web.interface.urls')),
)

from lisa.server.libs.server import enabled_plugins
for plugin in enabled_plugins:
    #try:
    urlpatterns += patterns('', url(r'^'+ str(plugin.lower()) + r'/', include(str(plugin) + '.web.urls')))
    v1_api.register(namedAny(plugin + '.web.api.' + plugin + 'Resource')())
    #except:
    #    pass

#Register plugin's API
urlpatterns += patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/docs/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
)
