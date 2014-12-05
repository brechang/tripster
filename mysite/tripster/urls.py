from django.conf.urls import patterns, url

from tripster import views

urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^auth', views.auth, name='auth'),
)
