from django.conf.urls import patterns, url

from plugins import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^install$', views.install, name='install')
)
