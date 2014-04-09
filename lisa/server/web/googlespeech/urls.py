from django.conf.urls import patterns, url

from lisa.server.web.googlespeech import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
