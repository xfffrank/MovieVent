from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
import datetime
from django.utils import timezone


# Create your models here.
class Movie(models.Model):
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:detail', args=[self.pk])

    name = models.CharField(max_length=100, unique=True)
    director = models.CharField(max_length=50)
    writer = models.CharField(max_length=150, null=True)
    star = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    region = models.CharField(max_length=30)
    language = models.CharField(max_length=100)
    release_time = models.CharField(max_length=100)
    duration = models.CharField(max_length=30)
    alternate_name = models.CharField(max_length=200, null=True)
    summary = models.TextField()
    poster = models.CharField(max_length=100)
    rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=5)
    heat = models.IntegerField(default=0)

    def is_now_playing(self):
        date = self.release_time.split('(')[0]
        try:
            trans_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            try:
                trans_date = datetime.datetime.strptime(date, '%Y-%m')
            except ValueError:
                trans_date = datetime.datetime.strptime(date, '%Y')

        now = timezone.now()
        # 60天内上映的电影
        return now - datetime.timedelta(days=60) < trans_date < now

# class CommentManager(models.Manager):
#     def create_comment(self, user, movie, text, thumb_ups):
#
#         comment = self.create(user_id=user, movie_id=movie, text=text, thumb_ups=thumb_ups)
#         return comment


class Comment(models.Model):

    def __str__(self):
        return self.text[:10]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=140)
    thumb_ups = models.IntegerField(default=0)


class Like(models.Model):
    """
    保存用户的点赞记录
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 点赞的用户
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE) # 所点赞的评论






