from django.shortcuts import render
from django.contrib.auth.models import User
from tripster import models
from django.contrib.auth import authentiate

# Create your views here.

def index(request):
    return render(request, 'tripster/index.html')

def register(request):
    username = request.POST['username']
    password = request.POST['password']
    affiliation = request.POST['affiliation']
    user = User.objects.create_user(username, password=password)
    user.save()
    t_user = models.TripsterUser(user=user, affiliation=affiliation)
    t_user.save()
    return render(request, 'tripster/auth.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        return render(request, 'tripster/home.html')
    else:
        error = "Incorrect login info!"
        return redirect('/', error=error)
