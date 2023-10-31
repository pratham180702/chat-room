from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Message, Topic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm, MessageForm
from django.db.models import Q
from django.contrib import messages

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Python room'},
#     {'id':2, 'name':'java room'},
#     {'id':3, 'name':'react room'},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        # added by me
        # Q(host__icontains=q)                        
        )
    
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request, 'base/home.html',context)

# def room_main(request):
#     context = {'id':0,'name':'MAIN ROOM'}
#     return render(request,'base/room.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=room)
    context = {'room':room, 'messages':messages}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def CreateRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id= pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not authorized to do this!")
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not authorized to do this!")

    if request.method =='POST':
        room.delete()
        return redirect('home')

    context = {'obj':room}
    return render(request, 'base/delete_room.html',context)


def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User doesn't exist!")
            return render(request, 'base/login_registration.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid password")

    context = {'page':page}
    return render(request, 'base/login_registration.html', context)


def registerPage(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
        
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('home')

    form = UserCreationForm()
    return render(request, 'base/login_registration.html', {'form':form})

def logoutPage(request):
    logout(request)
    return redirect('home')


# my added
def CreateMessage(request):
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/mess_form.html', context)
    