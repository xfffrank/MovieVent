from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    def __str__(self):
        return self.name

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


class comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    text = models.TextField()
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    thumb_ups = models.IntegerField(default=0)

