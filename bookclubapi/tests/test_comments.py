import datetime

from rest_framework import status
from rest_framework.test import APIClient
from bookclubapi.models import Book, Comment
from bookclubapi.serializers import BookSerializer
from .testbase import BookClubTestBase

# Create your tests here.
client = APIClient()


class CommentAPITests(BookClubTestBase):

    def setUp(self):
        self.user = BookClubTestBase.get_publisher('publisher', 'password')
        self.commentator = BookClubTestBase.get_basic('commentator', 'password')
        self.b1 = Book.objects.create(name="Test Book",
                                      publisher=self.user,
                                      publish_date=datetime.date(2020, 1, 1),
                                      Genre="test")

        self.c1 = Comment.objects.create(user=self.user,
                                         book=self.b1,
                                         content="test comment")

    def test_create_comment_fail(self):
        response = client.post('/comments/', data={
            'user': self.commentator.pk,
            'book': self.b1.pk,
            'content': 'test comment'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_success(self):
        client.force_authenticate(user=self.commentator)
        response = client.post('/comments/', data={
            'user': self.commentator.pk,
            'book': self.b1.pk,
            'content': 'test comment'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        client.force_authenticate(user=None)

    def test_get_comment(self):
        response = client.get(f'/comments/{self.c1.pk}/')
        comment = Comment.objects.get(id=self.c1.pk)
        serializer = BookSerializer(comment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_comment_fail(self):
        response = client.delete(f'/comments/{self.c1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_fail_not_self(self):
        client.force_authenticate(user=self.user)
        response = client.delete(f'/comments/{self.c1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_success(self):
        client.force_authenticate(user=self.commentator)
        response = client.delete(f'/comments/{self.c1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
