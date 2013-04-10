from django.conf.urls import patterns, url

from googlespeech import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
