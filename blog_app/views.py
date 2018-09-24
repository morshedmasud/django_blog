from django.shortcuts import render, get_object_or_404
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
    post = get_object_or_404(article, pk=id)
    context ={
        'post':post,
    }
    return render(request, "single.html", context)

def gettopic(request, name):
    return render(request, 'category.html')