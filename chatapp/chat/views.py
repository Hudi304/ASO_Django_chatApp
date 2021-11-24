from django.contrib.auth.forms import UserCreationForm
from django.core.checks import messages
from django.http.response import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# Create your views here.
from .models import Message, Room, ChatUser
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger("STUPED")


def index(request):
    return render(request, 'chat/index.html')

# def registerPage(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         form = CreateUserForm
#         context = {'form':  form}

#         if request.method == 'POST':
#             form = UserCreationForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 user = form.cleaned_data.get('username')
#                 messages.success(request, "Account wa create for " + user)
#                 return redirect('login')

#         return render(request, 'accounts/register.html', context)


def registerPage(request):
    form = CreateUserForm
    context = {'form':  form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account wa create for " + user)
            return redirect('login')

    return render(request, 'accounts/register.html', context)


# def registerPage(request):
#     form = CreateUserForm
#     context = {'form':  form}

#     username = request.POST.get("username")
#     logging.warning("---------------------from.data : " + username)
#     password = request.POST.get('password1')
#     logging.warning("---------------------from.data : " + password)
#     email = request.POST.get('email')
#     logging.warning("---------------------from.data : " + email)

#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')

#             # username = form.cleaned_data.get('username')
#             # password = form.cleaned_data.get('password1')
#             # email = form.cleaned_data.get('email')
#             logging.warning("---------------------from.data : " +
#                             username + " | " + password + " | " + email)

#             newChatUser = ChatUser.objects.create(
#                 username=username, password=password, email=email)
#             newChatUser.save()

#             messages.success(request, "Account wa create for ")
#             return redirect('login')
#     return render(request, 'accounts/register.html', context)


# def loginPage(request):
#     form = CreateUserForm
#     context = {'form':  form}
#     if request.user.is_authenticated:
#         return redirect('home')
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password = request.POST.get('password')

#             user = authenticate(request,  username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.info(request, 'Username or Password incorrect')

#         return render(request, 'accounts/login.html', context)


# def loginPage(request):
#     form = CreateUserForm
#     context = {'form':  form}

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request,  username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.info(request, 'Username or Password incorrect')

#     return render(request, 'accounts/login.html', context)


def loginPage(request):
    form = CreateUserForm
    context = {'form':  form}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,  username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password incorrect')

    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):

    # users = ChatUser.objects.all()
    context = {}

    # logging.error("users", users)

    return render(request, 'home.html', context)


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse()


def typing(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse()


def getMessages(request,  room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})
