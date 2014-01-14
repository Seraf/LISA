from django.conf.urls import patterns, include, url
from tastypie.api import Api
from manageplugins.api import PluginResource, IntentResource
from interface.api import WidgetResource, WorkspaceResource, WidgetByUserResource
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
    url(r'^speech/', include('googlespeech.urls')),
    url(r'^plugins/', include('manageplugins.urls')),
    url(r'', include('interface.urls')),
)

from libs.server import enabled_plugins
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
