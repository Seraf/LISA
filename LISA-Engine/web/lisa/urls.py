from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^plugins/', include('plugins.urls')),
    url(r'^speech/', include('googlespeech.urls')),
    url(r'', include('interface.urls')),
)
