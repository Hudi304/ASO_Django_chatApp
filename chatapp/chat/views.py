from django.contrib.auth.forms import UserCreationForm
from django.core.checks import messages
from django.http.response import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# Create your views here.
from .models import ChatRoom, Message
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger("STUPED")


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
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


def loginPage(request):
    form = CreateUserForm
    context = {'form':  form}
    if request.user.is_authenticated:
        return redirect('home')
    else:
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


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        roomName = request.POST['room_name']
        username = request.POST['username']

        logging.error('roomname : ', roomName, ' username : ', username)

        if ChatRoom.objects.filter(name=roomName).exists():
            return redirect('/' + roomName + '/?username=' + username)
        else:
            newRoom = ChatRoom.objects.create(name=roomName)
            newRoom.save()
            return redirect('/' + roomName + '/?username=' + username)

    context = {}
    return render(request, 'home.html', context)


def room(request, room):
    if request.method == 'GET':
        logging.error('GET  ')

        username = request.GET.get('username')
        # room_details = ChatRoom.objects.get(name=room)
        return render(request, 'room.html', {
            'username': username,
            'room': room,
            # 'room_details': room_details,
        })
    if request.method == 'PUT':
        # username = request.PUT.get('username')
        logging.error('PUT  ')

        return render(request, 'room.html', {
            'username': username,
            'room': room,
            # 'room_details': room_details,
        })


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id
    )

    new_message.save()

    # return HttpResponse('Hi message snet successfully!!')


def getMessages(request, room):
    room_details = ChatRoom.objects.get(name=room)
    logger.info('Something went wrong!')

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({
        'messages': list(messages.values())
    })


def checkview(request):
    roomName = request.POST['room_name']
    username = request.POST['username']

# if room name exists redirect to it
    if ChatRoom.objects.filter(name=roomName).exists():
        return redirect('/' + roomName + '/?username=' + username)
#  esle create room and redirect to it
    else:
        newRoom = ChatRoom.objects.create(name=roomName)
        newRoom.save()
        return redirect('/' + roomName + '/?username=' + username)
