from django.urls import path

from . import views
app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('pick/', views.pickMovie, name='pick'),
    path('now_playing', views.now_playing, name='now_playing'),
    # path('subject/<int: >', views.detail, name='detail'),
    path('subject/<int:movie_id>', views.detail, name='detail'),
    path('explore', views.explore, name='explore')
]