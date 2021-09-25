from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name='comment')
    content = models.CharField(max_length=100)
    time = models.DateTimeField(blank=False)

    def __str__(self):
        return f'{self.user}: {self.content} at {self.time}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name='post')
    content = models.CharField(max_length=100, blank=False)
    time = models.CharField(max_length=19)
    likes = models.IntegerField(default=0)
    comments = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, blank=True, related_name='post', null=True)
    likedUsers = models.ManyToManyField(User, blank=True, related_name='likedUsers')

    def __str__(self):
        return f'Post {self.id}: {self.content}'


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name="following")
    following = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, related_name="follower")

    def __str__(self):
        return f'{self.follower} is following {self.following}'