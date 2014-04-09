from django.conf.urls import patterns, url

from lisa.server.web.manageplugins import views

urlpatterns = patterns('',
    url(r'^list$', views.list, name='listplugins'),
)
