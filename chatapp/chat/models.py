from django.db import models

from datetime import datetime
# Create your models here.


# class ChatRoom(models.Model):
#     name = models.CharField(max_length=100)


# class Message(models.Model):
#     value = models.CharField(max_length=1000)
#     date = models.DateTimeField(default=datetime.now, blank=True)
#     room = models.CharField(max_length=100)
#     user = models.CharField(max_length=100)


class ChatUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Room(models.Model):
    name = models.CharField(max_length=1000)


# class Message(models.Model):
#     value = models.CharField(max_length=10000000)
#     date = models.DateTimeField(default=datetime.now, blank=True)
#     room = models.CharField(max_length=1000000)
#     user = models.CharField(max_length=1000000)
#     # tyr maging a message that is send on every button press that tells everyone in the room that the other user is typing
#     # userTyping = models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    room = models.CharField(max_length=1000, blank=True)
    user = models.CharField(max_length=100000)
    toUser = models.CharField(max_length=100000, blank=True)