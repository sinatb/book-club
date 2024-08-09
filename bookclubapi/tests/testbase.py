from bookclubapi.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase


class BookClubTestBase(TestCase):
    @staticmethod
    def get_publisher(username, password):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=f'{username}@mail.com',
            user_type='publisher'
        )
        token = Token.objects.create(user=user)

