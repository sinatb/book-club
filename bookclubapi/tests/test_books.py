import datetime

from rest_framework.test import APIClient
from rest_framework import status
from bookclubapi.models import Book, Comment
from bookclubapi.serializers import BookSerializer, CommentSerializer
from .fixture import BookClubFixture


# Create your tests here.


class BookAPITests(BookClubFixture):

    def setUp(self):
        self.user = BookClubFixture.get_publisher('publisher', 'password')
        self.b1 = Book.objects.create(name="Test Book",
                                      publisher=self.user,
                                      publish_date=datetime.date(2020, 1, 1),
                                      genre="test")

        self.b2 = Book.objects.create(name="Test Book 2",
                                      publisher=self.user,
                                      publish_date=datetime.date(2023, 1, 1),
                                      genre="test2")

        self.b3 = Book.objects.create(name="Test Book 3",
                                      publisher=self.user,
                                      publish_date=datetime.date(2025, 1, 1),
                                      genre="test")

        self.b4 = Book.objects.create(name="Test Book 4",
                                      publisher=self.user,
                                      publish_date=datetime.date(2003, 1, 1),
                                      genre="test2")

        self.c1 = Comment.objects.create(user=self.user,
                                         book=self.b1,
                                         content="test comment")

    def test_get_books(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_get_book(self):
        response = self.client.get(f'/books/{self.b3.pk}/')
        book = Book.objects.get(id=self.b3.pk)
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_unavailable_book(self):
        response = self.client.get('/books/30/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_book_unauthorized(self):
        response = self.client.post('/books/', data={
            'name': "Test Book 5",
            'publisher_id': self.user.pk,
            'publish_date': datetime.date(2033, 4, 3),
            'genre': 'test3'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_book_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/books/', data={
            'name': "Test Book 2",
            'publisher': self.user.pk,
            'publish_date': datetime.date(2033, 4, 3),
            'genre': 'test2'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.force_authenticate(user=None)

    def test_delete_book_unauthorized(self):
        response = self.client.delete(f'/books/{self.b3.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/books/{self.b3.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.b3.pk).exists())
        self.client.force_authenticate(user=None)

    def test_delete_missing_book(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('/books/30/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=None)

    def test_get_book_comments_unauthorized(self):
        response = self.client.get(f'/books/{self.b1.pk}/comments/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_book_comments_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/books/{self.b1.pk}/comments/')
        serializer = CommentSerializer(Comment.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate(user=None)

    def test_book_like_unauthorized(self):
        response = self.client.post(f'/books/{self.b3.pk}/like/', data={
            'book': self.b3.pk,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_like_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/books/{self.b3.pk}/like/', data={
            'book': self.b3.pk,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        b = Book.objects.get(pk=self.b3.pk)
        self.assertEqual(b.like_count, 1)
        self.client.force_authenticate(user=None)
