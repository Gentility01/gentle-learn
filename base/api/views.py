# from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializer import RoomSerializer


#trying to create an api for people to see the rooms in our application in there own application
@api_view(['GET']) #this will allow us get type of request we want example (get, post , put)
def getRoute(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)  
    # return JsonResponse(routes, safe=False)  #safe means we can use more than python dictionary in this (it will convert this to json list)
    
@api_view(['GET'])  
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True) #many means we will be serialing to many objets
    # return Response(rooms) #here object room cannot be returned or created like that so it needs to be serialized in the serialzer.py
    return Response(serializer.data) #passed serialized object


''' getting an endpoint that can allow users to open up a room in there website and view details about it'''
@api_view(['GET'])  
def getRoom(request, id):
    room = Room.objects.get(id=id)
    serializer = RoomSerializer(room, many=False) 
    # return Response(rooms) #here object room cannot be returned or created like that so it needs to be serialized in the serialzer.py
    return Response(serializer.data) #passed serialized object
    