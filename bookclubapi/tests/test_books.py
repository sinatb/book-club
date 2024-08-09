import datetime

from rest_framework.test import APIClient
from bookclubapi.models import Book
from bookclubapi.serializers import BookSerializer
from .testbase import BookClubTestBase

# Create your tests here.
client = APIClient()


class BookAPITests(BookClubTestBase):

    def setUp(self):
        self.user = BookClubTestBase.get_publisher('publisher', 'password')
        self.b1 = Book.objects.create(name="Test Book",
                                      publisher_id=self.user.id,
                                      publish_date=datetime.date(2020, 1, 1),
                                      Genre="test")

        self.b2 = Book.objects.create(name="Test Book 2",
                                      publisher_id=self.user.id,
                                      publish_date=datetime.date(2023, 1, 1),
                                      Genre="test2")

        self.b3 = Book.objects.create(name="Test Book 3",
                                      publisher_id=self.user.id,
                                      publish_date=datetime.date(2025, 1, 1),
                                      Genre="test")

        self.b4 = Book.objects.create(name="Test Book 4",
                                      publisher_id=self.user.id,
                                      publish_date=datetime.date(2003, 1, 1),
                                      Genre="test2")

    def test_get_books(self):
        response = client.get('/books/')
        self.assertEqual(response.status_code, 200)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_get_book(self):
        response = client.get('/books/3/')
        book = Book.objects.get(pk=self.b3.pk)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_get_unavailable_book(self):
        response = client.get('/books/30/')
        self.assertEqual(response.status_code, 404)

    def test_post_book_unauthorized(self):
        response = client.post('/books/', data={
            'name': "Test Book 5",
            'publisher_id': self.user.id,
            'publish_date': datetime.date(2033, 4, 3),
            'Genre': 'test3'
        })
        self.assertEqual(response.status_code, 401)

    def test_post_book_success(self):
        client.force_authenticate(user=self.user)
        response = client.post('/books/', data={
            'name': "Test Book 2",
            'publisher_id': self.user.id,
            'publish_date': datetime.date(2033, 4, 3),
            'Genre': 'test2'
        })
        self.assertEqual(response.status_code, 200)
        client.force_authenticate(user=None)

    def test_delete_book_unauthorized(self):
        response = client.delete('/books/3/')
        self.assertEqual(response.status_code, 401)

    def test_delete_book_success(self):
        client.force_authenticate(user=self.user)
        response = client.delete('/books/3/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Book.objects.filter(pk=self.b3.pk).exists())
        client.force_authenticate(user=None)

    def test_delete_missing_book(self):
        client.force_authenticate(user=self.user)
        response = client.delete('/books/30/')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Book.objects.filter(pk=self.b3.pk).exists())
        client.force_authenticate(user=None)
