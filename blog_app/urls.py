from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name="blog_app"

urlpatterns = [
    path('', views.index.as_view(), name='index'),
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
    # account confirmation
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # html to pdf
    path('pdf/<int:id>', views.Pdf.as_view(), name='pdf'),

    # path('article/<int:id>/like/', views.like_post, name='like_post'),
    path("article/<int:id>/like/", views.PostlikeToggle.as_view(), name='like_post'),
    path("api/<int:id>/like/", views.PostlikeAPIToggle.as_view(), name='api_like_post'),

]
