from django import forms
from .models import article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = article
        fields = [
            'article_author',
            'title',
            'body',
            'image',
            'category'
        ]