from django.urls import path
from .views import getRoute, getRooms, getRoom

urlpatterns = [
    path('', getRoute), 
    path('rooms/',getRooms),
    path('rooms/<int:id>/',getRoom)
]

#6:14:00