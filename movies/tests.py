from django.test import TestCase
from .models import Movie, Comment
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.


class MovieTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(
            name='test_movie',
            director = 'director',
            writer = 'writer',
            star = 'test_star',
            genre = 'action_movie',
            region = 'China',
            language = 'Chinese',
            release_time = '2018-09-09',
            duration = '123分钟',
            alternate_name = 'test_alt_name',
            summary = 'test_summary',
            poster = 'test_poster',
        )

    def test_movie_detail(self):
        movie = Movie.objects.get(name='test_movie')
        url = reverse('movies:detail', args=(movie.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



class CommentTestCase(TestCase):
    def setUp(self):
        movie = Movie.objects.create(
            name='test_movie',
            director='director',
            writer='writer',
            star='test_star',
            genre='action_movie',
            region='China',
            language='Chinese',
            release_time='2018-09-09',
            duration='123分钟',
            alternate_name='test_alt_name',
            summary='test_summary',
            poster='test_poster',
        )

        user = User.objects.create(username='test_user', password='123')

        Comment.objects.create(
            id = 2500,
            time = '2014-09-09',
            text = 'test_comment',
            thumb_ups = 0,
            movie_id = movie,
            user_id = user,
        )

    def test_like_comment(self):
        """
        not finished
        :return:
        """
        comment = Comment.objects.get(id = 2500)
        user = User.objects.get(username='test_user')
        self.client.post('/login/', {'username': 'test_user', 'password': '123'})
        url = reverse('movies:like_comment')
        response = self.client.post(url, {'comment_id': comment.id, 'user': user})
        self.assertEqual(response.status_code, 200)

        comment_update = Comment.objects.get(id=2500)
        self.assertEqual(comment_update.thumb_ups, 1)
