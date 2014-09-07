from django.conf.urls import patterns, include, url
from tastypie.api import Api
from lisa.server.web.manageplugins.api import PluginResource, IntentResource
from lisa.server.web.interface.api import WidgetResource, WorkspaceResource, WidgetByUserResource
from api.accounts import UserResource
from api.apilisa import LisaResource
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

urlpatterns = []

#Register plugin's API
from lisa.server.plugins.PluginManager import PluginManagerSingleton
for plugin in PluginManagerSingleton.get().getEnabledPlugins():
    urlpatterns += patterns('', url(r'^backend/' + str(plugin) + r'/', include('lisa.plugins.' +
                                                                       str(plugin) + '.web.urls')))
    v1_api.register(namedAny('lisa.plugins.' + plugin + '.web.api.' + plugin + 'Resource')())

apipatterns = patterns('',
    url(r'api/', include(v1_api.urls)),
    url(r'^api/docs/',
      include('tastypie_swagger.urls', namespace='tastypie_swagger'),
      kwargs={"tastypie_api_module":'lisa.server.web.weblisa.urls.v1_api', "namespace":"tastypie_swagger"}
    ),

)
urlpatterns += patterns('', (r'^backend/', include(apipatterns)))


