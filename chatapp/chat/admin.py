from django.contrib import admin

# Register your models here.


from .models import ChatRoom, Message, User

# ? adds modls to he admin site in order to make Crud operations on them
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(User)
