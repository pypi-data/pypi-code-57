from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class EditProfileForm(UserChangeForm):
    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
            'password': 'Password'
        }

        widgets = { 
            'username': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0'}),
            'first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0'}),
            'last_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0'}),
            'email': forms.EmailInput(attrs={'type': 'email', 'class': 'form-control rounded-0'})
        }