from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm
from django.db.models import Count

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


def home(request):
    q = request.GET.get('q', '')
    topic_id = request.GET.get('topic')
    if topic_id:
        rooms = Room.objects.filter(topic__id=topic_id, name__icontains=q)
    else:
        rooms = Room.objects.filter(name__icontains=q)
    topics = Topic.objects.annotate(room_count=Count('room'))
    room_count = rooms.count()
    room_messages = Message.objects.all().order_by('-created')[:10]
    context = {
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
        'room_count': room_count,
    }
    return render(request, 'principal/home.html', context)


def profile(request, id):
    user = get_object_or_404(User, username=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all().order_by('-created')[:10]
    context = {"user": user, 'rooms': rooms, 'room_messages': room_messages}
    return render(request, 'principal/profile.html', context)


@login_required
def room(request, id):
    room = get_object_or_404(Room, id=id)
    participants = room.participants.all()
    room_messages = room.message_set.all().order_by('-created')

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', id=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        'participants': participants
    }
    return render(request, 'principal/room.html', context)


@login_required
def createRoom(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = RoomForm()
    return render(request, 'principal/room_form.html', {
        'form': form, 'topics': topics, 'titulo': 'Crear sala'
    })


@login_required
def updateRoom(request, id):
    room = get_object_or_404(Room, id=id)
    if request.user != room.host:
        return HttpResponse('No tienes permiso para editar esta sala')
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = RoomForm(instance=room)
    return render(request, 'principal/room_form.html', {
        'form': form, 'topics': topics, 'titulo': 'Editar sala'
    })


@login_required
def deleteMessage(request, id):
    message = get_object_or_404(Message, id=id)
    if request.user != message.user:
        return HttpResponse('No tienes permiso para eliminar este mensaje')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'principal/delete.html', {'obj': message})


@login_required
def deleteRoom(request, id):
    room = get_object_or_404(Room, id=id)
    if request.user != room.host:
        return HttpResponse('No tienes permiso para eliminar esta sala')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'principal/delete.html', {'obj': room})
