from django.conf.urls import patterns, url
from tripster import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^feed', views.feed, name='feed'),
    url(r'^createtrip', views.create_trip, name='createtrip'),
    url(r'^settings', views.settings, name='settings'),
    url(r'^friends', views.friends, name='friends'),
    url(r'^view_trips', views.view_trips, name='view_trips'),
    url(r'^content/(?P<content_id>\d+)/$', views.get_content, name='get_content'),
    url(r'^trip/(?P<trip_id>\d+)/$', views.get_trip, name='get_trip'),
    url(r'^album/(?P<album_id>\d+)/$', views.get_album, name='get_album'),
    url(r'^createalbum$', views.create_album, name='createalbum'),
    url(r'^user/(?P<username>\w+)/$', views.get_userprofile, name='get_userprofile'),
    url(r'search', views.search, name='search'),
)

#if settings.DEBUG:
#    urlpatterns += patterns('',
#        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#        'document_root': settings.MEDIA_ROOT}))
