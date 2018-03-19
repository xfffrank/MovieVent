from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.core.paginator import Paginator
import re
from django.views import generic
# Create your views here.
from django.http import HttpResponse

# 该函数暂时不起任何作用
def index(request):
    return render(request, 'movies/index.html')
# class IndexView(generic.DetailView):
#     template_name = 'index.html'


def now_playing(request):
    movie_list = Movie.objects.order_by('-release_time')[:20] # 加'－'表示逆序

    for movie in movie_list:
        movie.name = movie.name.split(' ')[0]

    return render(request, 'movies/now_playing.html', {'movie_list': movie_list})

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    return render(request, 'movies/detail.html', {'movie': movie})

def explore(request):
    tag = request.GET.get('tag', '热门')

    if tag == '热门':
        movie_list = Movie.objects.order_by('-heat')[:50]
        pass
    elif tag == '最新':
        movie_list = Movie.objects.order_by('-release_time')
    else:
        movie_list = Movie.objects.filter(genre__icontains=tag)

    for movie in movie_list:
        movie.name = movie.name.split(' ')[0]

    # paginator
    limit = 15
    paginator = Paginator(movie_list, limit)
    page = request.GET.get('page')
    movies = paginator.get_page(page)

    context = {
        'movie_list': movies,
        'tag': tag,
    }

    return render(request, 'movies/pick_movie.html', context)
    # return HttpResponse(tag)

