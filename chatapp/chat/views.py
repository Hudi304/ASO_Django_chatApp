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

from django.db.models import Q

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger("STUPED")


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


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):

    # users = ChatUser.objects.all()
    context = {}

    # logging.error("users", users)

    return render(request, 'home.html', context)


@login_required(login_url='login')
def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
    })


@login_required(login_url='login')
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        # return redirect('/'+room+'/?username='+username)
        return redirect('room/'+room)

    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        # return redirect('/'+room+'/?username='+username)
        return redirect('room/' + room)


@login_required(login_url='login')
def send(request):
    message = request.POST['message']
    # username = request.POST['username']
    username = request.user

    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse()


@login_required(login_url='login')
def typing(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse()


@login_required(login_url='login')
def getMessages(request,  room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})


@login_required(login_url='login')
def selectUserForm(request):
    return render(request, 'privateMessage/selectUserForm.html')


@login_required(login_url='login')
def goToPrivateMessages(request):
    toUser = request.POST['user_name']
    try:
        checkUser = User.objects.get(username=toUser)
        return render(request, 'privateMessage/privateRoom.html', {
            'user_name': toUser
        })
    except User.DoesNotExist:
        return HttpResponseNotFound("<body><style> .body{  width: 100vw;height: 100vh; dispaly: flex;justify-content: center; align-items: center; }</style><p>User does not exist!</p></body>")


@login_required(login_url='login')
def getPrivateMessages(request):
    # user_name = request.POST['user_name']
    user_name = request.user

    messages = Message.objects.filter(Q(Q(toUser=user_name) & Q(
        user=request.user.username)) | Q(Q(toUser=request.user.username) & Q(user=user_name)))
    return JsonResponse({'messages': list(messages.values())})


@login_required(login_url='login')
def sendPm(request):
    message = request.POST['message']
    username = request.user.username
    user_name = request.POST['user_name']
    new_message = Message.objects.create(
        value=message, user=username, toUser=user_name
    )
    new_message.save()
    return HttpResponse("Message sent successfully!")


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


# def index(request):
#     return render(request, 'chat/index.html')

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
