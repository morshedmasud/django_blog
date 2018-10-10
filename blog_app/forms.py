from django import forms
from .models import article, author, Comment, category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = article
        fields = [
            'title',
            'body',
            'image',
            'category'
        ]

class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]


class CreateAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields = [
            'profile_pic',
            'details'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'email',
            'post_comment'
        ]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = "__all__"