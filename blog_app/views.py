from django.shortcuts import render, Http404, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from .models import author, category, article, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ArticleForm, RegisterUser, CreateAuthor, CommentForm, CategoryForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views import View
from .require import render_to_pdf
from django.template.loader import get_template
import datetime

# for mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from .token import activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# Create your views here.

class index(View):
    def get(self, request):
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
    get_comment = Comment.objects.filter(post=id)
    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.post=post
            instance.save()
            messages.success(request, 'Comment added')
    else:
        form = CommentForm

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    context ={
        'post':post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'first':first,
        'last':last,
        'related':related,
        'comments': get_comment,
        'form': form,
    }
    return render(request, "single.html", context)



def like_post(request):
    post = get_object_or_404(article, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    post_id = request.POST.get("post_id")
    return redirect("blog:single_post", post_id)



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
    return render(request, 'topic.html', context)


def getcreate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            instance = form.save(commit=False)
            instance.article_author=u
            instance.save()
            messages.info(request, "New Post created")
            return redirect('blog:profile')
        form = ArticleForm
        return render(request, 'create.html', {'form': form})
    else:
        return redirect('blog:login')


def getcategory(request):
    query = category.objects.all()
    content = {
        'all_category': query,
    }
    return render(request, 'category.html', content)

def createCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'New Category Added')
        return redirect('blog:category')
    form = CategoryForm
    return render(request, 'createCategory.html', {'form': form})

def deleteCategory(request, pk):
    print(pk)
    if request.user.is_authenticated:
        topic = get_object_or_404(category, id=pk)
        print(topic)
        topic.delete()
        messages.warning(request, "Category Deleted")
        return redirect('blog:category')
    else:
        return redirect('blog:login')

def updateCategory(request, pk):
    if request.user.is_authenticated:
        topic = get_object_or_404(category, id=pk)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=topic)
            form.save()
            messages.info(request, "Category updated")
            return redirect('blog:category')
        else:
            form = CategoryForm(instance=topic)
            return render(request, 'createCategory.html', {'form': form})
    else:
        return redirect('blog:login')

def getprofile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)
        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
            posts = article.objects.filter(article_author=authorUser.id)
            context = {
                'posts': posts,
                'user': authorUser
            }
            return render(request, 'loged_user.html', context)
        else:
            form = CreateAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                return redirect('blog:profile')
            return render(request, 'createauthor.html', {'form':form})
    else:
        return redirect('blog:login')


def getupdate(request, pk):
    if request.user.is_authenticated:
        post = article.objects.get(id=pk)
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=post)
            form.save()
            messages.success(request, 'Article updated successfully')
            return redirect('blog:profile')
        else:
            form = ArticleForm(instance=post)
            context = {'form': form}
            return render(request, 'create.html', context)
    else:
        return redirect('blog:login')


def getdelete(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=pk)
        post.delete()
        messages.warning(request, "Article is deleted.")
        return redirect('blog:profile')
    else:
        return redirect('blog:login')




# login, logout, Registration

def getlogin(request):
    if request.user.is_authenticated:
        return redirect('blog:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            auth = authenticate(request, username=username, password=password)
            if auth:
                login(request, auth)
                return redirect('blog:index')
            else:
                messages.add_message(request, messages.ERROR, 'Username or password mismatch.')
                # return render(request, 'login.html')
    return render(request, 'login.html')

def getlogout(request):
    logout(request)
    return redirect('blog:index')


def register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            print('current site--', current_site, current_site.domain)
            mail_subject = "Activate your blog account."
            message = render_to_string('confirm_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
                'token': activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse("<h2>Thanks for your registration. A confirmation link was sent to your email</h2>")
    else:
        form = RegisterUser()
    return render(request, 'register.html', {'form': form})


    # form = RegisterUser(request.POST or None)
    # if form.is_valid():
    #     instance = form.save(commit=False)
    #     instance.is_active=False
    #     instance.save()
    #     site=get_current_site(request)
    #     mail_subject = "Confirmation message for blog account"
    #     message = render_to_string('confirm_email.html', {
    #         'user':instance,
    #         'domain':site.domain,
    #         'uid':instance.id,
    #         'token': activation_token.make_token(instance)
    #     })
    #     to_email=form.cleaned_data.get('email')
    #     to_list = [to_email]
    #     from_email = settings.EMAIL_HOST_USER
    #     print(from_email)
    #     send_mail(mail_subject, message, from_email, to_list, fail_silently=False)
    #     return HttpResponse("<h2>Thanks for your registration. A confirmation link was sent to your email</h2>")

    # content = {
    #     'form': form,
    # }
    # return render(request, 'register.html', content)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid, 'uid decode')
        user = User.objects.get(id=uid)
        print(user)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("<h3>Thank you for your email confirmation. Now you can login your account. <a href='/login'>login</a></h3>")
    else:
        return HttpResponse("<h3>Activation link is invalid!</h3>")


# html to pdf

class Pdf(View):
    def get(self, request, id):
        try:
            query = get_object_or_404(article, id=id)
        except:
            Http404('Content not found!!')
        context = {
            'article': query,
        }
        pdf = render_to_pdf('pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            # pdf name generate with date
            date = datetime.date.today()
            tmpName = 'pdf'.split('.')[0]
            pdfName = tmpName+'-'+str(date)+'.pdf'
            content="inline; filename=%s" %(pdfName)
            download = request.GET.get('download')
            if download:
                content = "attachment; filename=%s" %(pdfName)
            response['Content-Disposition']=content
            return response
        return HttpResponse("NOT found")

