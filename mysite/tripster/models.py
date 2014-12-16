from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class TripsterUser(models.Model):
    # has (id), Username, password, firstname, lastname
    user = models.OneToOneField(User)
    affiliation = models.CharField(max_length=100)
    friends = models.ManyToManyField('self')
    url = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    dream_location = models.ManyToManyField('Location')
    privacy = models.IntegerField()

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Trip(models.Model):
    host = models.ForeignKey(TripsterUser)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    locations = models.ManyToManyField(Location)
    participants = models.ManyToManyField(TripsterUser, related_name='trips')
    timestamp = models.DateTimeField(default=timezone.now)
    privacy = models.IntegerField()
    class Meta:
        unique_together = ('host', 'name')
        ordering = ['-timestamp']

class Album(models.Model):
    name = models.CharField(max_length=100)
    trip = models.ForeignKey(Trip)
    timestamp = models.DateTimeField(default=timezone.now)
    privacy = models.IntegerField()
    class Meta:
        unique_together = ('name', 'trip')
        ordering = ['-timestamp']

class Content(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    album = models.ForeignKey(Album)
    timestamp = models.DateTimeField(default=timezone.now)
    privacy = models.IntegerField()
    class Meta:
        unique_together = ('album', 'name')
        ordering = ['-timestamp']

class TripComment(models.Model):
    user = models.ForeignKey(TripsterUser)
    trip = models.ForeignKey(Trip)
    comment = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['-timestamp']

class TripRating(models.Model):
    user = models.ForeignKey(TripsterUser)
    trip = models.ForeignKey(Trip)
    rating = models.IntegerField()
    class Meta:
        unique_together = ('user', 'trip')

class ContentComment(models.Model):
    user = models.ForeignKey(TripsterUser)
    content = models.ForeignKey(Content)
    comment = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['-timestamp']

class ContentRating(models.Model):
    user = models.ForeignKey(TripsterUser)
    content = models.ForeignKey(Content)
    rating = models.IntegerField()
    class Meta:
        unique_together = ('user', 'content')

class FriendRequest(models.Model):
    user = models.ForeignKey(TripsterUser)
    invitee = models.ForeignKey(TripsterUser, related_name='friend_requests')
    class Meta:
        unique_together = ('user', 'invitee')

class TripRequest(models.Model):
    invitee = models.ForeignKey(TripsterUser)
    trip = models.ForeignKey(Trip)
    class Meta:
        unique_together = ('invitee', 'trip')
