from pyexpat import model
from urllib.parse import MAX_CACHE_SIZE
from django.forms import ModelForm
from .models import *
from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Form_room(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'host','topic', 'description']
        exclude = ['host', 'patispant']
        
        
class Form_message(ModelForm):
    body = forms.CharField()
    class Meta:
        model = Message
        fields = ['body']
        
class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio'] 
        
       
class UserFormCreation(UserCreationForm):
    first_name = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder':'eg. John '}))
    last_name = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder':'eg. Doe '}))
    email = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder':'eg. john@gmail.com '}))
    username = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder':'eg. johndoe '}))
    password1 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'placeholder':'Enter password'}))
    password2 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'placeholder':'Repeat password'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        
        
     
