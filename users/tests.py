from django.test import TestCase
from .models import User
# Create your tests here.


class UsersTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='basic',
            password='basic1',
            email='basic@mail.com',
            user_type='basic'
        )

        User.objects.create_user(
            username='publisher',
            password='publisher1',
            email='pub@mail.com',
            user_type='publisher'
        )

    def test_users(self):
        basic = User.objects.get(user_type='basic')
        publisher = User.objects.get(user_type='publisher')
        self.assertEqual(basic.user_type, 'basic')
        self.assertEqual(publisher.user_type, 'publisher')
