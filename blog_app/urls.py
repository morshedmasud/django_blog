from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<name>', views.getauthor, name="author"),
    path('article/<int:id>', views.getsingle, name='single_post')
]