from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from tripster.models import *
from django.contrib.auth import authenticate, logout, login as django_login
from django.template import RequestContext, loader
from django.db.models import Q
import time
from pymongo import MongoClient

client = MongoClient()
db = client.cache_db
cache = db.cache
cache.remove()
# Create your views here.

def index(request):
    if request.method == "POST":
        logout(request)
    return render_to_response('tripster/index.html', RequestContext(request))

def register(request):
    if request.method == "GET":
        return render_to_response('tripster/register.html', RequestContext(request))
    if request.method == "POST":
        field_dict = dict()
        for field in ['username', 'password', 'affiliation', 'privacy', 'url', 'age', 'gender']:
            if field in request.POST and request.POST[field]:
                field_dict[field] = request.POST[field]
            else:
                return redirect('/register')

        user = User.objects.create_user(username=field_dict['username'], password=field_dict['password'])
        user.save()

        t_user = TripsterUser(user=user, affiliation=field_dict['affiliation'], url=field_dict['url'], age=field_dict['age'], gender=field_dict['gender'], privacy=field_dict['privacy'])
        t_user.save()
        return authenticate_user(request, field_dict['username'], field_dict['password'])

def authenticate_user(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        django_login(request, user)
        return redirect('/feed')
    else:
        error = "Incorrect login info!"
        return redirect('/', error=error)

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    return authenticate_user(request, username, password)

def score(user, trip):
    s = 0
    host = trip.host
    dream = user.dream_location.all()
    for l in trip.locations.all():
        if l in dream:
            s += 3
    for t in Trip.objects.all():
        p = t.participants.all()
        if user in p and host in p:
            s += 1
    return s

def score_trips(t_user):
    friend_trips = Trip.objects.filter(host__in=t_user.friends.all())
    your_trips = t_user.trips.all()
    trips = friend_trips.exclude(pk__in=your_trips)
    trips = list(trips)
    trips.sort(key = lambda t: -score(t_user, t))
    for t in trips:
        print score(t_user, t)
    return [trip.id for trip in trips][:10]

def feed(request):
    t_user = TripsterUser.objects.get(user=request.user)
    cache_dict = cache.find_one({'username': t_user.user.username})
    if cache_dict:
        print 'found in cache'
        print cache_dict
        if time.time() - cache_dict['timestamp'] > 30:
            trips = score_trips(t_user)
            cache.update(
                {'username': t_user.user.username},
                {'$set': {
                    'timestamp' : time.time(),
                    'trips' : trips,}
                },
            )
            cache_dict = cache.find_one({'username': t_user.user.username})
            print 'updated cache_dict'
            print cache_dict
    else:
        cache_dict = {'username': t_user.user.username, 'timestamp': time.time(), 'trips': score_trips(t_user)}
        id = cache.insert(cache_dict)
        print 'stored in cache ' + str(id)
        print cache_dict
    
    feed_dict = {
        'trips': Trip.objects.filter(id__in=cache_dict['trips'])
    }
    return render_to_response('tripster/home.html', feed_dict, RequestContext(request))

def friends(request):
    user = request.user
    t_user = TripsterUser.objects.get(user=user)
    if request.method == 'POST':
        if 'friend' in request.POST:
            friend_name = request.POST['friend']
            friend = User.objects.filter(username=friend_name)
            if friend:
                t_friend = TripsterUser.objects.get(user=friend)
                req = FriendRequest.objects.filter(user=t_user, invitee=t_friend)
                other_req = FriendRequest.objects.filter(user=t_friend, invitee=t_user)
                if t_friend != t_user and not req and not other_req and not t_friend in t_user.friends.all():
                    new_req = FriendRequest(user=t_user, invitee=t_friend)
                    new_req.save()
            return redirect('/friends')
        if 'accept' in request.POST:
            friend_name = request.POST['accept']
            friend = User.objects.get(username=friend_name)
            t_friend = TripsterUser.objects.get(user=friend)
            t_friend.friends.add(t_user)
            t_user.friends.add(t_friend)
            req = FriendRequest.objects.get(user=t_friend, invitee=t_user)
            req.delete()
            return redirect('/friends')
        if 'decline' in request.POST:
            friend_name = request.POST['decline']
            friend = User.objects.get(username=friend_name)
            t_friend = TripsterUser.objects.get(user=friend)
            req = FriendRequest.objects.get(user=t_friend, invitee=t_user)
            req.delete()
            return redirect('/friends')

    friend_requests = [f.user.user.username for f in t_user.friend_requests.all()]
    friends = t_user.friends.all()
    others = TripsterUser.objects.all().exclude(pk__in=friends).exclude(pk=t_user.id)[:10]
    friend_dict = {
        'friend_requests' : friend_requests,
        'friends' : friends,
        'others' : others,
        }
    return render_to_response('tripster/friends.html', friend_dict, RequestContext(request))

def create_trip(request):
    if request.method == "GET":
        return render_to_response('tripster/createtrip.html', RequestContext(request))
    if request.method == "POST":
        location = request.POST['location']
        name = request.POST['name']
        image = request.POST['image']
        privacy = request.POST['privacy']

        loc = Location.objects.filter(name=location)
        if not loc:
            loc = Location(name=location)
            loc.save()
        else:
            loc = loc[0]
        user = request.user
        t_user = TripsterUser.objects.get(user=user)
        trip = Trip(name=name, host=t_user, privacy=privacy)
        trip.save()
        trip.locations.add(loc)
        trip.participants.add(t_user)
        return redirect('/feed')

def settings(request):
    t_user = TripsterUser.objects.get(user=request.user)
    if request.method == "POST":
        location = request.POST['location'] if 'location' in request.POST else None
        if location is not None:
            if location:
                loc = Location.objects.filter(name=location)
                if not loc:
                    loc = Location(name=location)
                    loc.save()
                else:
                    loc = loc[0]
                t_user.dream_location.add(loc)
        else:
            affiliation = request.POST['affiliation']
            age = request.POST['age']
            gender = request.POST['gender']
            url = request.POST['url']
            privacy = request.POST['privacy']
            t_user.affiliation = affiliation
            t_user.age = age
            t_user.gender = gender
            t_user.url = url
            t_user.privacy = privacy
            t_user.save()

    settings_dict = {
        'user' : t_user,
        'dream_locations' : t_user.dream_location.all(),
    }
    return render_to_response('tripster/settings.html', settings_dict, RequestContext(request))

def view_trips(request):
    t_user = TripsterUser.objects.get(user=request.user)

    if request.method == "POST":
        if 'accept' in request.POST:
            request_id = request.POST['accept']
            trip_request = TripRequest.objects.get(pk=request_id)
            trip = trip_request.trip
            trip.participants.add(t_user)
            trip_request.delete()
        if 'decline' in request.POST:
            request_id = request.POST['decline']
            trip_request = TripRequest.objects.get(pk=request_id)
            trip_request.delete()

    trip_list = Trip.objects.filter(host=t_user)
    trip_requests = t_user.triprequest_set.all()
    trip_dict = {
                    'trip_list' : trip_list,
                    'trip_requests': trip_requests,
                    'joined_trip_list': t_user.trips.all(),
                }
    return render_to_response('tripster/trips.html', trip_dict, context_instance=RequestContext(request))

def get_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    triphost = trip.host
    tu = TripsterUser.objects.get(user=request.user)
    if tu != triphost and (trip.privacy == 0 or trip.privacy == 1 and tu not in triphost.friends.all()):
        return redirect('/feed')

    if request.method == "POST":
        location = request.POST['location'] if 'location' in request.POST else None
        participant = request.POST['participant'] if 'participant' in request.POST else None
        comment = request.POST['comment'] if 'comment' in request.POST else None
        rating = request.POST['rating'] if 'rating' in request.POST else None
        privacy = request.POST['privacy'] if 'privacy' in request.POST else None
        if location:
            loc = Location.objects.filter(name=location)
            if not loc:
                loc = Location(name=location)
                loc.save()
            else:
                loc = loc[0]
            trip.locations.add(loc)
        if participant:
            user = User.objects.filter(username=participant)
            if user:
                t_user = TripsterUser.objects.get(user=user)
                req = TripRequest.objects.filter(trip=trip, invitee=t_user)
                if not req and not t_user in trip.participants.all():
                    new_req = TripRequest(trip=trip, invitee=t_user)
                    new_req.save()
        if comment:
            t_user = TripsterUser.objects.get(user=request.user)
            c = TripComment(user=t_user, trip=trip, comment=comment)
            c.save()
        if rating:
            t_user = TripsterUser.objects.get(user=request.user)
            r = TripRating.objects.filter(user=t_user, trip=trip)
            if r:
                r = r[0]
                r.rating = rating
                r.save()
            else:
                r = TripRating(user=t_user, trip=trip, rating=rating)
                r.save()
        if privacy:
            trip.privacy = privacy
    t_user = TripsterUser.objects.get(user=request.user)
    locations = trip.locations.all()
    participants = trip.participants.all()
    comments = trip.tripcomment_set.all()
    rating = TripRating.objects.filter(user=t_user, trip=trip)

    # privacy for albums (and in general):
    # 0 = only me, 1 = all my friends, 2 = global
    albums = Album.objects.filter(trip=trip)
    if trip.host != t_user:
        albums.exclude(privacy=0)
        if t_user not in trip.host.friends.all():
            albums.exclude(privacy=1)

    trip_info = {
            'trip' : trip,
            'locations_list' : locations,
            'participants' : participants,
            'trip_id' : trip_id,
            'comments' : comments,
            'range' : range(1,6),
            'albums' : albums,
    }

    if rating:
        trip_info.update({'rating': rating[0]})
    if tu == trip.host:
        trip_info.update({ 'is_host' : True })
    return render_to_response('tripster/trip.html', trip_info, RequestContext(request))

def create_album(request):
    t_user = TripsterUser.objects.get(user=request.user)
    trips = t_user.trips.all()
    trip_list = { 'trips' : trips }
    if request.method == "GET":
        return render_to_response('tripster/createalbum.html', trip_list, RequestContext(request))
    if request.method == "POST":
        name = request.POST['name']
        privacy = request.POST['privacy']
        trip_id = request.POST['trip_id']
        trip = Trip.objects.get(id=trip_id)

        album = Album(name=name, trip=trip, privacy=privacy)
        album.save()
        return redirect('/feed')

def get_album(request, album_id):
    album = Album.objects.get(id=album_id)
    contents = Content.objects.filter(album=album)
    triphost = album.trip.host
    tu = TripsterUser.objects.get(user=request.user)
    if tu != triphost and (album.privacy == 0 or album.privacy == 1 and tu not in triphost.friends.all()):
        return redirect('/feed')

    # add content
    if request.method == "POST":
        name = request.POST['name'] if 'name' in request.POST else None
        url = request.POST['url'] if 'url' in request.POST else None
        a_privacy = request.POST['a_privacy'] if 'a_privacy' in request.POST else None
        c_privacy = request.POST['c_privacy'] if 'c_privacy' in request.POST else None
        if name and url and album:
            content = Content(name=name, url=url, album=album, privacy=c_privacy)
            content.save()
        if a_privacy:
            album.privacy = a_privacy

    if tu != triphost:
        contents.exclude(privacy=0)
        if tu not in album.trip.host.friends.all():
            contents.exclude(privacy=1)


    album_info = {
        'album' : album,
        'trip_name' : album.trip.name,
        'contents' : contents,
    }

    if tu == triphost:
        album_info.update({ 'is_owner' : True })

    return render_to_response('tripster/album.html', album_info, RequestContext(request))

def get_content(request, content_id):
    content = Content.objects.get(id=content_id)
    triphost = content.album.trip.host
    t_user = TripsterUser.objects.get(user=request.user)
    if t_user != triphost and (content.privacy == 0 or content.privacy == 1 and t_user not in triphost.friends.all()):
        return redirect('/feed')

    comments = ContentComment.objects.filter(content=content)
    if request.method == "POST":
        comment = request.POST['comment'] if 'comment' in request.POST else None
        rating = request.POST['rating'] if 'rating' in request.POST else None
        privacy = request.POST['privacy'] if 'privacy' in request.POST else None
        if comment:
            t_user = TripsterUser.objects.get(user=request.user)
            c = ContentComment(user=t_user, content=content, comment=comment)
            c.save()

        if rating:
            t_user = TripsterUser.objects.get(user=request.user)
            r = ContentRating.objects.filter(user=t_user, content=content)
            if r:
                r = r[0]
                r.rating = rating
                r.save()
            else:
                r = ContentRating(user=t_user, content=content, rating=rating)
                r.save()
        if privacy:
            content.privacy = privacy
    content_info = {
            'content' : content,
            'comments': comments,
            'range' : range(1,6),
        }
    if t_user == content.album.trip.host:
        content_info.update({'is_owner': True})

    rating = ContentRating.objects.filter(user=t_user, content=content)
    if rating:
        content_info.update({'rating': rating[0]})
    comment = request.POST['comment'] if 'comment' in request.POST else None
    return render_to_response('tripster/content.html', content_info, RequestContext(request))

def get_userprofile(request, username):
    tu = TripsterUser.objects.get(user=request.user)
    user_prof = TripsterUser.objects.filter(user__username=username)[0]
    if not user_prof:
        redirect('/feed')
    if tu != user_prof and (user_prof.privacy == 0 or user_prof.privacy == 1 and tu not in user_prof.friends.all()):
        return redirect('/feed')

    t_user = user_prof
    dream_location_list = [d.name for d in t_user.dream_location.all()]
    trips_list = Trip.objects.filter(host=t_user)
    visited_locations = [l for t in trips_list for l in t.locations.all()]
    friends_list = [f.user for f in t_user.friends.all()]
    user_info = {
            't_user' : t_user,
            'username' : username,
            'user_profile_pic' : t_user.url,
            'dream_location_list': dream_location_list,
            'trips_list' : trips_list,
            'friends_list' : friends_list,
            'visited_locations' : visited_locations,
        }
    return render_to_response('tripster/user.html', user_info, RequestContext(request))

def search(request):
    search_info = {}
    if request.method == "POST":
        key = request.POST['search'].lower()
        locations = []
        users = []
        for loc in Location.objects.all():
            if key in loc.name.lower():
                locations.append(loc)
        for u in TripsterUser.objects.all():
            if key in u.user.username.lower():
                users.append(u)
        search_info = {
            'locations' : locations,
            'users' : users,
        }
    return render_to_response('tripster/search.html', search_info, RequestContext(request))
