from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('pick/', views.pick, name='pick'), # 这个不能删，有毒
    path('explore/', views.explore, name='explore'),
    path('reviews/', views.reviews, name='reviews'),
    path('now_playing', views.now_playing, name='now_playing'),
    # path('subject/<int: >', views.detail, name='detail'),
    path('subject/<int:movie_id>', views.detail, name='detail'),
    path('subject/<int:movie_id>/post_comment', views.post_comment, name='post_comment'),
    path('subject/<int:movie_id>/del_comment/<int:comment_id>', views.del_comment, name='del_comment'),
    path('subject/<int:movie_id>/comments', views.all_comments, name='all_comments'),
    path('subject_search', views.subject_search, name='subject_search'),
]