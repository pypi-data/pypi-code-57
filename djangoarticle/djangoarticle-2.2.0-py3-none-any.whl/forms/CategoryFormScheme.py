from django import forms
from django.forms import ModelForm
from djangoarticle.models import CategoryModelScheme


class CategoryFormScheme(ModelForm):
    class Meta:
        model   = CategoryModelScheme
        fields  = ['serial', 'title', 'description', 'status']

        labels  = {
            'serial': 'Post number',
            'title': 'Category title',
            'description': 'Category description',
            'status': 'Status'
        }

        widgets = {
            'serial': forms.NumberInput(attrs={'class': 'form-control rounded-0', 'type': 'numbers'}),
            'title': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0', 'placeholder':'Category title'}),
            'status': forms.Select(attrs={'class': 'custom-select rounded-0'}),
            'description': forms.Textarea(attrs={'type': 'text', 'rows': '5', 'class': 'form-control border-0 rounded-0', 'placeholder':'Article description'})
        }