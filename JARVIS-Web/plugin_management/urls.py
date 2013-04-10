from django.conf.urls import patterns, url

from plugin_management import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
