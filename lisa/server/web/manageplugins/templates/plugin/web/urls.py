from django.conf.urls import patterns, url
from {{ plugin_name }}.web import views

urlpatterns = patterns('',
    url(r'^$',views.index),
)
