from django.forms import ModelForm
from .models import CommentSection


class CommentForm(ModelForm):
    class Meta:
        model = CommentSection
        fields = ('username', 'email', 'body')

