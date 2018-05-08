from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(username='test_user', password='123')

    def test_get_users(self):
        self.assertIsNotNone(
            User.objects.get(username='test_user')
        )

    def test_modify_user(self):
        user = User.objects.get(username='test_user')
        user.username = 'test_user2'
        user.save()
        self.assertEqual(user.username, 'test_user2')

    def test_account(self):
        user = User.objects.get(username='test_user')
        user.set_password('123')
        user.save()
        login = self.client.login(username='test_user', password='123')

        url = reverse('users:account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_center(self):
        user = User.objects.get(username='test_user')
        user.set_password('123')
        user.save()
        login = self.client.login(username='test_user', password='123')

        url = reverse('users:homepage', args=(user.id, ))
        response = self.client.get(url)
        self.assertEqual(response.context['username'], 'test_user')

    def test_delete_account(self):
        user = User.objects.get(username='test_user')
        user.set_password('123')
        user.save()

        login = self.client.login(username='test_user', password='123')
        self.assertIs(login, True)
        url = reverse('users:delete_account')
        self.client.get(url)

        test = User.objects.all()
        self.assertQuerysetEqual(test, [])







class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail(
                subject="这是新的密码,请使用新的密码登录",
                message='123',
                from_email='m15211180180@163.com',
                recipient_list=['546706835@qq.com',],
                fail_silently=False,
            )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, '这是新的密码,请使用新的密码登录')