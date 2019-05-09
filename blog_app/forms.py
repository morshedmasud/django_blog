from django import forms
from .models import article, author, Comment, category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = article
        fields = [
            'title',
            'video',
            'body',
            'image',
            'category'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RegisterUser(UserCreationForm):
    email = forms.EmailField(max_length=200, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email..'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password ...',}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password ...',}))

    # class Meta:
    #     model = User
    #     fields = ('username', 'first_name', 'last_name', 'email')


    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        )

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Password didn't match")
        else:
            return cd['password2']


class CreateAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields = [
            'profile_pic',
            'details'
        ]


class CommentForm(forms.ModelForm):
    post_comment = forms.CharField(widget=forms.Textarea(attrs={"class": 'form-control', 'cols': 40, 'rows': 4, 'placeholder': 'Say something... ' }), label='')
    class Meta:
        model = Comment
        fields = [
            'post_comment'
        ]
        # widgets = {
        #     # 'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     # 'email': forms.TextInput(attrs={"class": 'form-control'}),
        #     'post_comment': forms.Textarea(attrs={"class": 'form-control', 'cols':30, 'rows': 5, 'placeholder': 'Say something... ' })
        # }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = "__all__"
