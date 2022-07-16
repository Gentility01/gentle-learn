from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Room, Topic, Message, User
from .forms import Form_room, Form_message, ProfileForm, UserFormCreation
# from django.contrib.auth.models import User


# Create your views here.

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower() #converts any uppercase to lowercase
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnot exist')
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'User or password doesnot exist')
            
        
    return render(request,'base/login_register.html',{'page':page})

def logOut(request):
    logout(request)
    return redirect('home')

def registerUser(request):
  
    form = UserFormCreation()
    if request.method == 'POST':
        form = UserFormCreation(request.POST)
        if form.is_valid():
            #freezing and accessing the user. reason: if a user adds in an uppercase i want to change it to lowercase
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            #accessing the user tO login authomatically then move to the home page
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {
        'form':form
    }
    return render(request,'base/login_register.html', context)
    

def home(request):
    '''icontains will makesure what ever value we have in our topic
    name contains what we have in 'q' whic is our request.GET.get and Q can help us to use ANd and OR'''
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))  
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    # room_messages = Message.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
        'room_messages':room_messages
        }
    return render(request,'base/home.html', context)



def responsive_topic(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)) 
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count
    }
    return render(request, 'base/topics.html', context)


def responsive_activity(request):
    room_messages =Message.objects.all()
    # room_messages = room.message_set.all().order_by('-created')
    # paticipants = room.patispant.all()
    context = {
        # 'room_messages':room_messages,
        # 'paticipants':paticipants,
        'room_messages':room_messages
        
    }
    return render(request,'base/activity.html', context)

def room(request, id):
    room = get_object_or_404(Room, id=id)
    room_messages = room.message_set.all().order_by('-created')  #message_set gets the child object of room i.e the forignkey of that room
    paticipants = room.patispant.all()  #when we use many to many fields we dont need to add _set to get the child
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            body = request.POST.get('body')
            
        )
        
        return redirect('room', id=room.id)
    context = {
        'room':room,
        'room_messages':room_messages,
        'paticipants':paticipants,
        # 'message':message
    }
    room.patispant.add(request.user)  #to add user authomaticallyy to the patiscipant whic is in our many to many fields
    return render(request, 'base/room.html', context)



@login_required(login_url='loginPage')
def createRoom(request):
    form = Form_room()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name) #this will return back an object in the form if it is created already but if it is not it will create a new object
        
        # form = Form_room(request.POST)
        
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        Room.objects.create(
            host = request.user,
            topic =topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
            
        )
        return redirect('home')
    context = {
        'form':form,
        'topics':topics
    }
    return render(request,'base/base_form.html', context)



def userProfile(request, id):
    user = get_object_or_404(User, id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,
               'rooms':rooms,
               'room_messages':room_messages,
               'topics':topics
               }
    return render(request,'base/profile.html', context)



@login_required(login_url='loginPage')
def updateRoom(request, id):
    room = get_object_or_404(Room, id=id)
    form = Form_room(instance=room)
    topics = Topic.objects.all()
    
    #restricting user not edit to another users room
    if request.user != room.host:
        return HttpResponse('Not allowed here!!!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # form = Form_room(request.POST, instance=room)
        # if form.is_valid():
        #         form.save()
        return redirect('home')
    context = {
        'form':form,
        'topics':topics,
        'room':room
    }
    
    return render(request,'base/base_form.html', context)


def updateMessage(request, id):
    page = 'update'
    message = get_object_or_404(Message, id=id)
    form = Form_message(instance=message)
    
    #restricting user not edit to another users room
    if request.user != message.user:
        return HttpResponse('Not allowed here!!!')
    
    if request.method == 'POST':
        form = Form_message(request.POST, instance=message)
        if form.is_valid():
                form.save()
                return redirect('home')
    context = {
        'form':form,
        'page':page
    }
    return render(request, 'base/room.html', context)


@login_required(login_url='loginPage')
def deleteRoom(request, id):
    room = get_object_or_404(Room, id=id)
     #restricting user not delete to another users room
    if request.user != room.host:
        return HttpResponse('Not allowed here!!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})




@login_required(login_url='loginPage')
def deleteMessage(request, id):
    message = get_object_or_404(Message, id=id)
     #restricting user not delete to another users message
    if request.user != message.user:
        return HttpResponse('Not allowed here!!!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='loginPage')
def updateUser(request):
    user = request.user
    form = ProfileForm(instance=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile', id=user.id )
    context = {
        'form':form
    }
    return render(request,'base/update-user.html', context)


    