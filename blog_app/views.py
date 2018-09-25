from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import author, category, article
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ArticleForm
# Create your views here.

def index(request):
    posts = article.objects.all()
    search = request.GET.get('q')
    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    paginator = Paginator(posts, 8) # Show 8 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        'posts': total_article,
    }
    return render(request, "index.html", context)

def getauthor(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(author, name=post_author.id)
    posts = article.objects.filter(article_author=auth.id)
    paginator = Paginator(posts, 4) # Show 8 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        'auth': auth,
        'posts': total_article
    }
    return render(request, "profile.html", context)

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
    paginator = Paginator(posts, 4) # Show 8 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        'posts':total_article,
        'category':cat,
    }
    return render(request, 'category.html', context)


def getlogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        print("not authen")
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            auth = authenticate(request, username=username, password=password)
            if auth:
                login(request, auth)
                return redirect('index')
    return render(request, 'login.html')

def getlogout(request):
    logout(request)
    return redirect('index')

def getcreate(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            form.save()
            return redirect('index')
        form = ArticleForm
        return render(request, 'create.html', {'form': form})
    else:
        return redirect('login')