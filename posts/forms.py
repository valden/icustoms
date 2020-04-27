from django import forms
from .models import Topic, Post, Comment


class TopicForm(forms.ModelForm):
    """Topic form for creating and updating topics"""
    class Meta:
        model = Topic
        fields = ('title', 'image', 'description', 'closed')
        exclude = ('author', 'updated', 'created')


class PostForm(forms.ModelForm):
    """Post form for creating and updating posts"""
    class Meta:
        model = Post
        fields = ('author', 'title', 'preview', 'image', 'content')
        exclude = ('updated', 'created')


class CommentForm(forms.ModelForm):
    """Comment form for creating and updating comments"""
    class Meta:
        model = Comment
        fields = ('post', 'content')
        widgets = {'post': forms.HiddenInput()}
        exclude = ('created', 'updated')
