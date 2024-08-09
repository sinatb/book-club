from bookclubapi.models import User
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
        return user
    @staticmethod
    def get_basic(username, password):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=f'{username}@mail.com',
            user_type='basic'
        )
        return user