from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'', include('interface.urls')),
    url(r'^plugins/', include('plugins.urls')),
    url(r'^speech/', include('googlespeech.urls')),
)
