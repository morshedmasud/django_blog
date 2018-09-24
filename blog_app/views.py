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
    first = article.objects.first()
    last = article.objects.last()
    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    context ={
        'post':post,
        'first':first,
        'last':last,
        'related':related,
    }
    return render(request, "single.html", context)

def gettopic(request, name):
    cat = get_object_or_404(category, name=name)
    posts = article.objects.filter(category=cat.id)
    context = {
        'posts':posts,
        'category':cat,
    }
    return render(request, 'category.html', context)