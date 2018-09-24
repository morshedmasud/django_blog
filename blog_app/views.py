from django.shortcuts import render
from .models import author, category, article
# Create your views here.

def index(request):
    posts = article.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, "index.html", context)

def getauthor(request, name):
    return render(request, "profile.html")

def getsingle(request, id):
    return render(request, "single.html")