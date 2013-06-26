from django.conf.urls import patterns, url

from plugins import views

urlpatterns = patterns('',
    url(r'^list$', views.list, name='listplugins'),
    url(r'^install$', views.install, name='install'),
    url(r'^uninstall$', views.uninstall, name='uninstall'),
    url(r'^enable$', views.enable, name='enable'),
    url(r'^disable$', views.disable, name='disable'),
)
