from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import re
from django.views import generic
# Create your views here.
from django.http import HttpResponse


def pick(request):
    return render(request, 'movies/pick_movie.html')

def now_playing(request):
    def recent():
        # 写一个判断日期的函数
        pass

    movie_list = Movie.objects.order_by('-release_time')[:20] # 加'－'表示逆序

    for movie in movie_list:
        movie.name = movie.name.split(' ')[0]

    return render(request, 'movies/now_playing.html', {'movie_list': movie_list})

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    return render(request, 'movies/detail.html', {'movie': movie})

def explore(request):

    tag = request.GET.get('tag', '热门')
    sort = request.GET.get('sort', 'recommend')
    print(tag, sort)

    if sort == 'recommend':
        sort_value = '-heat'
    elif sort == 'time':
        sort_value = '-release_time'
    elif sort == 'rank':
        sort_value = '-rating'

    if tag == '热门':
        if sort == 'recommend':
            movie_list = Movie.objects.all().order_by('-heat')
        elif sort == 'time':
            movie_list = Movie.objects.order_by('-heat')[:50]
            movie_list = sorted(movie_list, key=lambda m: m.release_time, reverse=True)
        elif sort == 'rank':
            movie_list = Movie.objects.order_by('-heat')[:50]
            movie_list = sorted(movie_list, key=lambda m: m.rating, reverse=True)
    elif tag == '最新':
        # 需设置 radio 不可选
        movie_list = Movie.objects.all().order_by('-release_time')
    else:
        movie_list = Movie.objects.filter(genre__icontains=tag).order_by(sort_value)

    for movie in movie_list:
        movie.name = movie.name.split(' ')[0]

    # paginator
    limit = 15
    paginator = Paginator(movie_list, limit)
    page = request.GET.get('page')
    print('当前页数', page)
    movies = paginator.get_page(page)

    context = {
        'movie_list': movies,
        'tag': tag,
        'sort': sort,
    }

    return render(request, 'movies/pick_movie.html', context)
    # return HttpResponse(tag)


def index(request):

    # 正在上映
    now_playing = Movie.objects.order_by('-release_time')[:20]
    for movie in now_playing:
        movie.name = movie.name.split(' ')[0]

    limit = 5
    paginator1 = Paginator(now_playing, limit)
    now_playing_page = request.GET.get('now_playing_page')
    now_playing = paginator1.get_page(now_playing_page)

    # 热门电影
    hot_list = Movie.objects.order_by('-heat')[:20]
    for movie in hot_list:
        movie.name = movie.name.split(' ')[0]

    paginator2 = Paginator(hot_list, limit)
    hot_page = request.GET.get('hot_page')
    hot_list = paginator2.get_page(hot_page)

    # 口碑榜
    rating_list = Movie.objects.order_by('-rating')[:20]
    for movie in rating_list:
        movie.name = movie.name.split(' ')[0]

    paginator2 = Paginator(rating_list, limit)
    rating_page = request.GET.get('rating_page')
    rating_list = paginator2.get_page(rating_page)

    context = {
        'movie_list1': now_playing,
        'hot_list': hot_list,
        'rating_list': rating_list,
        'now_playing_page': now_playing_page,
        'hot_page': hot_page,
        'rating_page': rating_page,
    }



    return render(request, 'movies/index.html', context)



