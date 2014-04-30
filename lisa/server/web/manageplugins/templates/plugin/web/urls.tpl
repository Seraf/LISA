from django.conf.urls import patterns, url
from lisa.plugins.{{ plugin_name }}.web import views

urlpatterns = patterns('',
    url(r'^$',views.index),
)
