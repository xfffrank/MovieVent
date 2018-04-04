"""
根据每部电影的评论数计算热度heat
"""
from movies.models import Comment, Movie

movie_list = Movie.objects.all()

for movie in movie_list:
    movie.heat = movie.comment_set.count()
    movie.save()

