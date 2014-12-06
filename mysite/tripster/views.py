from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from tripster import models
from django.contrib.auth import authenticate, login as django_login
from django.template import RequestContext

# Create your views here.

def index(request):
    return render_to_response('tripster/index.html', RequestContext(request))

def signup(request):
    return render_to_response('tripster/register.html', RequestContext(request))

def register(request):
    username = request.POST['username']
    password = request.POST['password']
    affiliation = request.POST['affiliation']
    user = User.objects.create_user(username, password=password)
    user.save()
    t_user = models.TripsterUser(user=user, affiliation=affiliation)
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

