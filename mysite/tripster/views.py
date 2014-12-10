from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from tripster.models import *
from django.contrib.auth import authenticate, login as django_login
from django.template import RequestContext, loader
from django.db.models import Q

# Create your views here.

def index(request):
    return render_to_response('tripster/index.html', RequestContext(request))

def register(request):
    if request.method == "GET":
        return render_to_response('tripster/register.html', RequestContext(request))
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        affiliation = request.POST['affiliation']
        user = User.objects.create_user(username, password=password)
        user.save()
        t_user = TripsterUser(user=user, affiliation=affiliation)
        t_user.save()
        return authenticate_user(request, username, password)

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

def feed(request):
    t_user = TripsterUser.objects.get(user=request.user)
    trips = Trip.objects.filter(Q(host__in=t_user.friends.all()) | Q(host=t_user))
    feed_dict = {
        'trips' : trips,
    }
    return render_to_response('tripster/home.html', feed_dict, RequestContext(request))

def friends(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            user = request.user
            t_user = TripsterUser.objects.get(user=user)
            friend_requests = [f.user.user.username for f in t_user.friend_requests.all()]
            friends = [f.user.username for f in t_user.friends.all()]
            friend_dict = {
                'friend_requests' : friend_requests,
                'friends' : friends,
                }
            return render_to_response('tripster/friends.html', friend_dict, RequestContext(request))
        else:
            return redirect('/')

    if request.method == 'POST':
        if request.user.is_authenticated():
            user = request.user
            t_user = TripsterUser.objects.get(user=user)
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
                else:
                    # no friend found
                    # redirect to home with error message
                    return redirect('/friends')
            elif 'accept' in request.POST:
                friend_name = request.POST['accept']
                friend = User.objects.get(username=friend_name)
                t_friend = TripsterUser.objects.get(user=friend)
                t_friend.friends.add(t_user)
                t_user.friends.add(t_friend)
                req = FriendRequest.objects.get(user=t_friend, invitee=t_user)
                req.delete()
                return redirect('/friends')
            else:
                # we fucked up
                return redirect('/friends')
        else:
            # not authenticated go to login
            return redirect('/')

def create_trip(request):
    if request.method == "GET":
        return render_to_response('tripster/createtrip.html', RequestContext(request))
    if request.method == "POST":
        location = request.POST['location']
        name = request.POST['name']
        image = request.POST['image']

        loc = Location.objects.filter(name=location)
        if not loc:
            loc = Location(name=location)
            loc.save()
        else:
            loc = loc[0]
        if request.user.is_authenticated():
            user = request.user
            t_user = TripsterUser.objects.get(user=user)
            trip = Trip(name=name, host=t_user)
            trip.save()
            trip.locations.add(loc)
            trip.participants.add(t_user)
            return redirect('/feed')

def change_settings(request):
    return render_to_response('tripster/settings.html', RequestContext(request))

def settings(request):
    affiliation = request.POST['affiliation']
    user = request.user
    t_user = TripsterUser.objects.get(user=user)
    t_user.affiliation = affiliation
    t_user.save()
    return redirect('/feed')

def view_trips(request):
    t_user =  TripsterUser.objects.get(user=request.user)

    if request.method == "POST":
        request_id = request.POST['accept']
        trip_request = TripRequest.objects.get(pk=request_id)
        trip = trip_request.trip
        trip.participants.add(t_user)
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
    trip = Trip.objects.filter(id=trip_id)[0]
    if request.method == "POST":
        location = request.POST['location'] if 'location' in request.POST else None
        participant = request.POST['participant'] if 'participant' in request.POST else None
        comment = request.POST['comment'] if 'comment' in request.POST else None
        rating = request.POST['rating'] if 'rating' in request.POST else None
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
    t_user = TripsterUser.objects.get(user=request.user)
    locations = trip.locations.all()
    participants = trip.participants.all()
    comments = trip.tripcomment_set.all()
    rating = TripRating.objects.filter(user=t_user, trip=trip)
    albums = Album.objects.filter(trip=trip)
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
    return render_to_response('tripster/trip.html', trip_info, RequestContext(request))

def create_album(request):
    trips = Trip.objects.all()
    trip_list = { 'trips' : trips }
    if request.method == "GET":
        return render_to_response('tripster/createalbum.html', trip_list, RequestContext(request))
    if request.method == "POST":
        name = request.POST['name']
        trip_id = request.POST['trip_id']
        trip = Trip.objects.get(id=trip_id)

        album = Album(name=name, trip=trip)
        album.save()

        return redirect('/feed')

def get_album(request, album_id):
    album = Album.objects.filter(id=album_id)[0]
    contents = Content.objects.filter(album=album)
    # add content
    if request.method == "POST":
        name = request.POST['name'] if 'name' in request.POST else None
        url = request.POST['url'] if 'url' in request.POST else None

        if name and url and album:
            content = Content(name=name, url=url, album=album)
            content.save()

    album_info = {
            'album' : album,
            'trip_name' : album.trip.name,
            'contents' : contents,
    }

    return render_to_response('tripster/album.html', album_info, RequestContext(request))

def get_content(request, content_id):
    content = Content.objects.get(id=content_id)
    comments = ContentComment.objects.filter(content=content)
    if request.method == "POST":
        comment = request.POST['comment'] if 'comment' in request.POST else None
        rating = request.POST['rating'] if 'rating' in request.POST else None
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

    content_info = {
            'content' : content,
            'comments': comments,
            'range' : range(1,6),
    }
    t_user = TripsterUser.objects.get(user=request.user)
    rating = ContentRating.objects.filter(user=t_user, content=content)
    if rating:
        content_info.update({'rating': rating[0]})
    comment = request.POST['comment'] if 'comment' in request.POST else None
    return render_to_response('tripster/content.html', content_info, RequestContext(request))

def search(request):
    search_info = {}
    if request.method == "POST":
        key = request.POST['search']
        locations = []
        users = []
        for loc in Location.objects.all():
            if key in loc.name:
                locations.append(loc)
        for u in TripsterUser.objects.all():
            if key in u.user.username:
                users.append(u)
        serach_info = {
            'locations' : locations,
            'users' : users,
        }
    return render_to_response('tripster/search.html', search_info, RequestContext(request))
