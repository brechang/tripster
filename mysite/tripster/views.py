from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from tripster.models import *
from django.contrib.auth import authenticate, login as django_login
from django.template import RequestContext, loader

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
    return render_to_response('tripster/home.html', RequestContext(request))

def add_friend(request):
    friend_name = request.POST['friend']
    if request.user.is_authenticated():
        user = request.user
        t_user = TripsterUser.objects.get(user=user)
        friend = User.objects.filter(username=friend_name)
        if friend:
            t_friend = TripsterUser.objects.get(user=friend)
            req = FriendRequest.objects.filter(user=t_user, invitee=t_friend)
            if req:
                # already made request
                pass
            else:
                new_req = FriendRequest(user=t_user, invitee=t_friend)
                new_req.save()
        else:
            # no friend found
            # redirect to home with error message
            pass
    else:
        # not authenticated go to login
        pass

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
            trip.save()
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
    trip_list = Trip.objects.all()
    trip_dict = { 'trip_list' : trip_list }
    return render_to_response('tripster/mytrips.html', trip_dict, context_instance=RequestContext(request))

def get_trip(request):
    if request.method == "GET":
        t_user = TripsterUser.objects.get(user=request.user)
        trip_name = request.path.split('/')[-2]
        trip = Trip.objects.filter(name=trip_name, host=t_user)[0]
        locations = trip.locations.all()
        participants = trip.participants.all()
        trip_info = {
                'trip' : trip,
                'locations_list' : locations,
                'participants' : participants
        }
        return render_to_response('tripster/trip.html', trip_info, RequestContext(request))

