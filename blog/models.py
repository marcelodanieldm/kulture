from django.db import models

# Create your models here.
# blog/models.py

from django.db import models
from users.models import CustomUser


class BlogCategory(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    thumbnail = models.ImageField(upload_to='blog_thumbnails/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_share_url(self):
        return f"/blog/{self.id}/share/"

    def get_detail_url(self):
        return f"/blog/{self.id}/"
