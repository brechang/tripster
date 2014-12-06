from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TripsterUser(models.Model):
    # has (id), Username, password, firstname, lastname
    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=100)
    friends = models.ManyToManyField('self')
    dream_location = models.ManyToManyField('Location')

class Location(models.Model):
    name = models.CharField(max_length=100)

class Trip(models.Model):
    host = models.ForeignKey(TripsterUser)
    trip_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    locations = models.ManyToManyField(Location)
    participants = models.ManyToManyField(TripsterUser, related_name='trips')

class Album(models.Model):
    name = models.CharField(max_length=100)
    trip = models.ForeignKey(Trip)

class Content(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    album = models.ForeignKey(Album)

class TripComment(models.Model):
    user = models.ForeignKey(TripsterUser)
    trip = models.ForeignKey(Trip)
    comment = models.CharField(max_length=2000)
    rating = models.IntegerField()

class ContentComment(models.Model):
    user = models.ForeignKey(TripsterUser)
    content = models.ForeignKey(Content)
    comment = models.CharField(max_length=2000)
    rating = models.IntegerField()

class FriendRequest(models.Model):
    user = models.ForeignKey(TripsterUser)
    invitee = models.ForeignKey(TripsterUser, related_name='requests')
