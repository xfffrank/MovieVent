from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
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

    def test_delete_user(self):
        user = User.objects.create(username='test_user3', password='123')
        user.delete()

    def login(self):
        response = self.client.post('/login/', {'username': 'test_user', 'password': '123'})
        self.assertEqual(response.status_code, 200)




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