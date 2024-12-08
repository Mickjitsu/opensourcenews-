from django import forms
from .models import Article, Category, Comment

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']