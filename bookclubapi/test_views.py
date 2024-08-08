import datetime

from django.test import TestCase, Client

from bookclubapi.models import Book, User

# Create your tests here.
client = Client()


class BookAPITests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='publisher',
                                        email='<EMAIL>',
                                        password='<PASSWORD>',
                                        user_type="publisher")

        Book.objects.create(name="Test Book",
                            publisher_id=user.id,
                            publish_date=datetime.date(2020, 1, 1),
                            Genre="test")

        Book.objects.create(name="Test Book 2",
                            publisher_id=user.id,
                            publish_date=datetime.date(2023, 1, 1),
                            Genre="test2")

        Book.objects.create(name="Test Book",
                            publisher_id=user.id,
                            publish_date=datetime.date(2025, 1, 1),
                            Genre="test")

        Book.objects.create(name="Test Book 2",
                            publisher_id=user.id,
                            publish_date=datetime.date(2003, 1, 1),
                            Genre="test2")


def test_get_books(self):
        pass
        # all_books = Book.objects.all()
        # assert all_books[0].publish_date < all_books[1].publish_date
