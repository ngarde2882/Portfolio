from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    #remember_me = forms.BooleanField()
    class Meta:
        model = Profile
        fields = ['image', 'start_time', 'end_time', 'remember_me']