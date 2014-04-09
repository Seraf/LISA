from django.conf.urls import patterns, url

from lisa.server.web.interface import views

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
)
