from django.urls import path
# from .views import home,room, createRoom, updateRoom, deleteRoom,loginPage,logOut,registerUser
from .views import *
urlpatterns = [
    path('', home, name='home'),
    path('responsive-topic', responsive_topic, name='responsive_topic'),
    path('responsive_activity', responsive_activity, name='responsive_activity'),
    path('update-user', updateUser, name='updateUser'),
    path('profile/<int:id>/', userProfile, name='userProfile'),
    path('login', loginPage, name='loginPage'),
    path('logout', logOut, name='logOut'),
    path('register', registerUser, name='registerUser'),
    path('createRoom', createRoom, name='createRoom'),
    path('delete/<int:id>/', deleteRoom, name='deleteRoom'),
    path('deleteroom/<int:id>/', deleteMessage, name='deleteMessage'),
    path('update/<int:id>/', updateRoom, name='updateRoom'),
    path('updatemessage/<int:id>/', updateMessage, name='updateMessage'),
    path('room/<int:id>/', room, name='room'),
]
