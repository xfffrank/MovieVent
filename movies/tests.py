from django.test import TestCase
from .models import Movie, Comment
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.


class MovieTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(
            name='test_movie1',
            director = 'director',
            writer = 'writer',
            star = 'test_star',
            genre = 'action_movie',
            region = 'China',
            language = 'Chinese',
            release_time = '2018-03-09',
            duration = '123分钟',
            alternate_name = 'test_alt_name',
            summary = 'test_summary',
            poster = 'test_poster',
        )

        Movie.objects.create(
            name='test_movie2',
            director='director',
            writer='writer',
            star='test_star',
            genre='action_movie',
            region='China',
            language='Chinese',
            release_time='2018-04-01',
            duration='123分钟',
            alternate_name='test_alt_name',
            summary='test_summary',
            poster='test_poster',
        )

    def test_movie_detail(self):
        movie = Movie.objects.get(name='test_movie1')
        url = reverse('movies:detail', args=(movie.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_movie1')

    def test_movie_index(self):
        response = self.client.get(reverse('movies:index'))
        self.assertQuerysetEqual(
            response.context['np_list'],
            ['<Movie: test_movie1>', '<Movie: test_movie2>']
        )
        self.assertQuerysetEqual(
            response.context['hot_list'],
            ['<Movie: test_movie1>', '<Movie: test_movie2>']
        )
        self.assertQuerysetEqual(
            response.context['rating_list'],
            ['<Movie: test_movie1>', '<Movie: test_movie2>']
        )

    def test_movie_explore(self):
        response = self.client.get(reverse('movies:explore'), {'tag': '热门', 'sort': 'recommend'})
        self.assertContains(response, 'test_movie1')

    def test_movie_now_playing(self):
        url = reverse('movies:now_playing')
        response = self.client.get(url)
        self.assertQuerysetEqual(
            response.context['movie_list'],
            ['<Movie: test_movie1>', '<Movie: test_movie2>']
        )


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

        user = User.objects.create(username='test_user', password='123456')

        Comment.objects.create(
            id = 1,
            time = '2014-09-09',
            text = 'test_comment',
            thumb_ups = 0,
            movie_id = movie,
            user_id = user,
        )

    def test_all_comments(self):
        movie = Movie.objects.get(name='test_movie')
        url = reverse('movies:all_comments', args=(movie.id,))
        response = self.client.get(url)
        self.assertContains(response, 'test_comment')

    def test_movie_reviews(self):
        url = reverse('movies:reviews')
        response = self.client.get(url, {'sort': 'time'})
        self.assertContains(response, 'test_comment')

    # def test_like_comment(self):
    #     """
    #     not finished
    #     :return:
    #     """
    #     comment = Comment.objects.get(id = 2500)
    #     user = User.objects.get(username='test_user')
    #     print('已创建用户：', user)
    #     res = self.client.login(username='Feng', password='xf5797877')
    #     print('登陆状态：', res)
    #     url = reverse('movies:like_comment')
    #     response = self.client.post(url, {'comment_id': comment.id, 'user': user})
    #     print(response.context)
    #
    #     self.assertEqual(response.status_code, 200)
    #
    #     comment_update = Comment.objects.get(id=2500)
    #     self.assertEqual(comment_update.thumb_ups, 1)
