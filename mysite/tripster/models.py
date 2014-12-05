from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TripsterUser(models.Model):
    # has (id), Username, password, firstname, lastname
    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=100)

class Location(models.Model):
    name = models.CharField(max_length=100)

class Trip(models.Model):
    host = models.ForeignKey(TripsterUser)
    location = models.ForeignKey(Location)

class Album(models.Model):
    name = models.CharField(max_length=100)
    trip = models.ForeignKey(Trip)

class Content(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    album = models.ForeignKey(Album)

class FriendsWith(models.Model):
    user1 = models.ForeignKey(TripsterUser)
    user2 = models.ForeignKey(TripsterUser)

class ParticipantsOf(models.Model):
    user = models.ForeignKey(TripsterUser)
    trip = models.ForeignKey(Trip)

class DreamLocationOf(models.Model):
    user = models.ForeignKey(TripsterUser)
    name = models.ForeignKey(Location)

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

