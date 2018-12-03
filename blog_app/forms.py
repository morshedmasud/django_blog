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


class RegisterUser(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Password didn't match")
        else:
            return cd['password2']

    # class Meta:
    #     model = User
    #     fields = [
    #         'first_name',
    #         'last_name',
    #         'email',
    #         'username',
    #         'password1',
    #         'password2'
    #     ]


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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={"class": 'form-control'}),
            'post_comment': forms.Textarea(attrs={"class": 'form-control'})
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = "__all__"
