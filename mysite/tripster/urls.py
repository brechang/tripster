from django.conf.urls import patterns, url

from tripster import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^feed', views.feed, name='feed'),
    url(r'^make_trip', views.make_trip, name='make_trip'),
    url(r'^newtrip', views.newtrip, name='newtrip'),
    url(r'^change_settings', views.change_settings, name='change_settings'),
    url(r'^settings', views.settings, name='settings'),
#    url(r'^trips', views.my_trips, name='my_trips'),
#    url(r'^friends', views.my_friends, name='my_friends'),
#    url(r'^search', views.search, name='search')
    url(r'^add_friend', views.add_friend, name='add_friend'),
)

