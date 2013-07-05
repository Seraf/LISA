from django.conf.urls import patterns, url

from plugins import views

urlpatterns = patterns('',
    url(r'^list$', views.list, name='listplugins'),
)
