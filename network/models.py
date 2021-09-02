from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    #likedPosts = models.ForeignKey(Post, on_delete=models.DO_NOTHING, blank=True, related_name='user')
    pass


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name='comment')
    content = models.CharField(max_length=100)
    time = models.DateTimeField(blank=False)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name='post')
    content = models.CharField(max_length=100, blank=False)
    time = models.CharField(max_length=19)
    likes = models.IntegerField(default=0)
    comments = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, blank=True, related_name='post', null=True)


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name="following")
    following = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name="follower")


# Need to impliment liked posts