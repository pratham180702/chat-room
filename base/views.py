from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Message, Topic
from .forms import RoomForm, MessageForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Python room'},
#     {'id':2, 'name':'java room'},
#     {'id':3, 'name':'react room'},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(topic__name__icontains = q)
    topics = Topic.objects.all()
    context = {'rooms':rooms,'topics':topics}
    return render(request, 'base/home.html',context)

# def room_main(request):
#     context = {'id':0,'name':'MAIN ROOM'}
#     return render(request,'base/room.html',context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=room)
    context = {'room':room, 'messages':messages}
    return render(request, 'base/room.html', context)



def CreateRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html',context)



def updateRoom(request, pk):
    room = Room.objects.get(id= pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'base/room_form.html',context)



def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method =='POST':
        room.delete()
        return redirect('home')

    context = {'obj':room}
    return render(request, 'base/delete_room.html',context)


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
    