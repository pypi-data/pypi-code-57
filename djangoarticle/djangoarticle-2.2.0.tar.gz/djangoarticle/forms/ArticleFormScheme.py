from django import forms
from django.forms import ModelForm
from djangoarticle.models import ArticleModelScheme


class ArticleFormScheme(ModelForm):
    class Meta:
        model = ArticleModelScheme

        fields = [ 'serial', 'cover_image', 'title', 'category', 'description',
                   'shortlines', 'content', 'status', 'total_views', 'verification',
                   'is_promote', 'is_trend', 'is_promotional', 'is_opinion']

        labels = { 'serial': 'Serial Number',
                   'cover_image': 'Cover image',
                   'title': 'Title',
                   'category': 'Category',
                   'description': 'Description',
                   'shortlines': 'Shortlines',
                   'content': 'Content',
                   'status': 'Status',
                   'total_views': 'Total views',
                   'verification': 'Verify',
                   'is_promote': 'Promote',
                   'is_trend': 'Trend',
                   'is_promotional': 'Promotional',
                   'is_opinion': 'Opinion'
        }
        
        widgets = { 'serial': forms.NumberInput(attrs={'class': 'form-control rounded-0', 'type': 'numbers'}),
                    'cover_image': forms.FileInput(attrs={'type': 'file', 'class': 'custom-file-input rounded-0'}),
                    'title': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0','placeholder':'Article title'}),
                    'status': forms.Select(attrs={'class': 'custom-select rounded-0'}),
                    'category': forms.Select(attrs={'class': 'custom-select rounded-0'}),
                    'description': forms.Textarea(attrs={'type': 'text', 'class': 'form-control border-0 rounded-0', 'rows': '5', 'placeholder':'Article description'}),
                    'shortlines': forms.Textarea(attrs={'type': 'text', 'class': 'form-control border-0 rounded-0', 'rows': '5', 'placeholder':'Article shortlines'}),
                    'content': forms.Textarea(attrs={'type': 'text', 'class': 'form-control border-0 rounded-0', 'id': 'mytextarea', 'rows': '20', 'placeholder':'Article content'}),
                    'total_views': forms.NumberInput(attrs={'class': 'form-control rounded-0', 'type': 'numbers'}),
                    'verification': forms.CheckboxInput(attrs={}),
                    'is_promote': forms.CheckboxInput(attrs={}),
                    'is_trend': forms.CheckboxInput(attrs={}),
                    'is_promotional': forms.CheckboxInput(attrs={}),
                    'is_opinion': forms.CheckboxInput(attrs={})
        }