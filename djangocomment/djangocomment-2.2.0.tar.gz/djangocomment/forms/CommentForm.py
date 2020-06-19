from django import forms
from djangocomment.models import CommentModel


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['content']
        labels = {"content": "Comment"}

        widgets = {
            "content": forms.Textarea(attrs={'class': 'form-control rounded-0', 'id': 'commentInput', 'rows': '2'})
        }