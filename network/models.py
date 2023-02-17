from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    def __str__(self):
        return self.username


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_post")
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.content

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow', null=True)
    followers = models.ManyToManyField(User, related_name='followers')
    following = models.ManyToManyField(User, related_name='following')

    def __str__(self):
        return self.user.username
