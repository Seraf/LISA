from django.conf.urls import patterns, include, url
from tastypie.api import Api
from plugins.api import PluginResource
from api import LisaResource

v1_api = Api(api_name='v1')
v1_api.register(PluginResource())
v1_api.register(LisaResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^speech/', include('googlespeech.urls')),
    url(r'^plugins/', include('plugins.urls')),
    url(r'', include('interface.urls')),
)
