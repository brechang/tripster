from django.conf.urls import patterns, url

from tripster import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^feed', views.feed, name='feed'),
    url(r'^createtrip', views.create_trip, name='createtrip'),
    url(r'^change_settings', views.change_settings, name='change_settings'),
    url(r'^settings', views.settings, name='settings'),
    url(r'^friends', views.friends, name='friends'),
    url(r'^view_trips', views.view_trips, name='view_trips'),
    url(r'^trip/(?P<trip_id>\d+)/$', views.get_trip, name='get_trip'),
)

