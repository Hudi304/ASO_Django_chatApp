from .models import Room, Message
from django.contrib import admin

# Register your models here.


from .models import Message, ChatUser, Room

# ? adds modls to he admin site in order to make Crud operations on them
admin.site.register(ChatUser)
admin.site.register(Room)
admin.site.register(Message)
