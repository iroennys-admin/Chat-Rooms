from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


rooms = [
    {"id": 1, "name": "Sergio"},
    {"id": 2, "name": "Pablo"},
    {"id": 3, "name": "Miguel"},
]

def home(request):
    q = request.GET.get('q','')
    topic_id = request.GET.get('topic')
    if topic_id:
        rooms = Room.objects.filter(topic__id = topic_id, name__icontains = q)
    else:
        rooms = Room.objects.filter(name__icontains = q)
    topics = Topic.objects.all()

    room_messages = Message.objects.all()
    context = {'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'principal/home.html', context )



def profile(request, id):
    user = User.objects.get(username = id)
    rooms = user.room_set.all()
    context = {"user": user, 'rooms': rooms}
    return render(request, 'principal/profile.html', context )




@login_required
def room(request, id):  
    room = Room.objects.get(id=id)
    participants = room.participants.all()
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', id=room.id)
        
    context = {"room": room, "room_messages": room_messages, 
                'participants': participants}  
    return render(request, 'principal/room.html', context)
@login_required
def createRoom(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            room = form.save(commit = False)
            room.host = request.user
            room.save()
            return redirect('home')
    else:
        form = RoomForm()
    return render(request, 'principal/room_form.html', {'form': form })
   

@login_required
def deleteMessage(request, id):
    message = Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'principal/delete.html', {'obj': message})


def deleteRoom(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('No tienes acceso a esto')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'principal/delete.html', {'obj': room})    

    
    






