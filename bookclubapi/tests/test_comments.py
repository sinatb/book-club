import datetime

from rest_framework import status
from bookclubapi.models import Book, Comment
from bookclubapi.serializers import CommentSerializer
from .fixture import BookClubFixture

# Create your tests here.


class CommentAPITests(BookClubFixture):

    def setUp(self):
        self.user = BookClubFixture.get_publisher('publisher', 'password')
        self.commentator = BookClubFixture.get_basic('commentator', 'password')
        self.b1 = Book.objects.create(name="Test Book",
                                      publisher=self.user,
                                      publish_date=datetime.date(2020, 1, 1),
                                      genre="test")

        self.c1 = Comment.objects.create(user=self.user,
                                         book=self.b1,
                                         content="test comment")

    def test_create_comment_fail(self):
        response = self.client.post('/comments/', data={
            'user': self.commentator.pk,
            'book': self.b1.pk,
            'content': 'test comment'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment_success(self):
        self.client.force_authenticate(user=self.commentator)
        response = self.client.post('/comments/', data={
            'user': self.commentator.pk,
            'book': self.b1.pk,
            'content': 'test comment'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.force_authenticate(user=None)

    def test_get_comment(self):
        self.client.force_authenticate(user=self.commentator)
        response = self.client.get(f'/comments/{self.c1.pk}/')
        comment = Comment.objects.get(id=self.c1.pk)
        serializer = CommentSerializer(comment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data, serializer)
        self.assertEqual(response.data, serializer.data)
        self.client.force_authenticate(user=None)

    def test_delete_comment_fail(self):
        response = self.client.delete(f'/comments/{self.c1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_fail_not_self(self):
        self.client.force_authenticate(user=self.commentator)
        response = self.client.delete(f'/comments/{self.c1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=None)

    def test_delete_comment_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/comments/{self.c1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.force_authenticate(user=None)

    def test_get_comments_reports_unauthorized(self):
        response = self.client.get(f'/comments/{self.c1.pk}/reports/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comments_reports_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/comments/{self.c1.pk}/reports/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)
