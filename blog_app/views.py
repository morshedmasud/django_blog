from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import author, category, article
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ArticleForm
from django.contrib import messages
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
    print(total_article, "y---------")
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
    print('last id:', last.id)
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
            else:
                messages.add_message(request, messages.ERROR, 'Username or password mismatch.')
                # return render(request, 'login.html')
    return render(request, 'login.html')

def getlogout(request):
    logout(request)
    return redirect('index')

def getcreate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        print(u, '---------')
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            instance = form.save(commit=False)
            instance.article_author=u
            instance.save()
            messages.info(request, "New Post created")
            return redirect('profile')
        form = ArticleForm
        return render(request, 'create.html', {'form': form})
    else:
        return redirect('login')


def getprofile(request):
    if request.user.is_authenticated:
        posts = article.objects.filter(article_author=request.user.id)
        user = get_object_or_404(author, name=request.user.id)
        context = {
            'posts': posts,
            'user': user
        }
        return render(request, 'loged_user.html', context)


def getupdate(request, pk):
    if request.user.is_authenticated:
        post = article.objects.get(id=pk)
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=post)
            form.save()
            messages.success(request, 'Article updated successfully')
            return redirect('profile')
        else:
            form = ArticleForm(instance=post)
            context = {'form': form}
            return render(request, 'create.html', context)
    else:
        return redirect('login')


def getdelete(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=pk)
        post.delete()
        messages.warning(request, "Article is deleted.")
        return redirect('profile')
    else:
        return redirect('login')