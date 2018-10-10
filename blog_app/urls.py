from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name="blog_app"

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<name>', views.getauthor, name="author"),
    path('article/<int:id>', views.getsingle, name='single_post'),
    path('topic/<name>', views.gettopic, name='topic'),
    path('login/', views.getlogin, name="login"),
    path('logout', views.getlogout, name='logout'),
    path('create', views.getcreate, name='create'),
    path('profile', views.getprofile, name='profile'),
    path('update/<int:pk>', views.getupdate, name='update'),
    path('delete/<int:pk>', views.getdelete, name='delete'),
    path('register/', views.register, name='register'),
    path('category/', views.getcategory, name='category'),
    path('createCategory/', views.createCategory, name='createCategory'),
    path('updateCategory/<pk>', views.updateCategory, name='updateCategory'),
    path('deleteCategory/<int:pk>', views.deleteCategory, name='deleteCategory'),
]

# if settings.DEBUG:
#     urlpatterns+=static(settings.STATIC_URL,  document_root=settings.STATIC_ROOT)
#     urlpatterns+=static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
