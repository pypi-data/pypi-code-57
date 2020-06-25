from django import forms
from django.forms import ModelForm
from djangoadmin.models import UserModel


class UserForm(ModelForm):
    class Meta:
        model = UserModel
        fields = ['image', 'address', 'phone', 'website']

        labels = {
            'image': 'Profile image',
            'address': 'Address',
            'phone': 'Phone',
            'website': 'Website',
        }

        widgets = { 
            'image': forms.ClearableFileInput(attrs={}),
            'address': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0'}),
            'phone': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control rounded-0'}),
            'website': forms.URLInput(attrs={'type': 'url', 'class': 'form-control rounded-0'})
        }