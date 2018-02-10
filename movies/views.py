from django.shortcuts import render
from django.views import generic
# Create your views here.
from django.http import HttpResponse

# 该函数暂时不起任何作用

def index(request):
    return render(request, 'movies/index.html')
# class IndexView(generic.DetailView):
#     template_name = 'index.html'