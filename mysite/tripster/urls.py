from django.conf.urls import patterns, url

from tripster import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^feed', views.feed, name='feed'),
    url(r'^settings', views.feed, name='settings'),
    url(r'^trips', views.feed, name='my_trips'),
    url(r'^friends', views.feed, name='my_friends'),
    url(r'^newtrip', views.feed, name='new_trip'),
    url(r'^search', views.feed, name='search')
)

