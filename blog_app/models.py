from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.FileField(upload_to = 'author_pic/')
    details = models.TextField()

    def __str__(self):
        return self.name.username


class category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class article(models.Model):
    article_author = models.ForeignKey(author, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    video = models.TextField(null=True, blank=True)
    body= RichTextUploadingField()
    likes = models.ManyToManyField(User, related_name='likes',blank=True)
    image = models.FileField(upload_to = 'product_image/')
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_on = models.DateField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    def get_single_url(self):
        return reverse('blog:single_post', kwargs={"id":self.pk})

    def total_likes(self):
        return self.likes.count()

    def get_author_url(self):
        return reverse('blog:author', kwargs={"name":self.article_author})

    def get_topic_url(self):
        return reverse("blog:topic", kwargs={"name":self.category})

    def get_like_url(self):
        return reverse('blog:like_post', kwargs={"id":self.pk})

    def get_api_like_url(self):
        return reverse('blog:api_like_post', kwargs={"id":self.pk})



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(article, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.CASCADE)
    post_comment = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.post.title, self.user.username)
