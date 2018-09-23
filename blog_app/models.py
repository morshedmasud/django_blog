from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return self.name


class category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class article(models.Model):
    article_author = models.ForeignKey(author, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    body=models.TextField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title