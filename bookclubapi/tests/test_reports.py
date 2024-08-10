import datetime

from rest_framework import status
from bookclubapi.models import Book, Comment, Report
from bookclubapi.serializers import ReportSerializer
from .fixture import BookClubFixture

# Create your tests here.


class ReportAPITests(BookClubFixture):
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

        self.r1 = Report.objects.create(user=self.user,
                                        comment=self.c1,
                                        reason="test report")

    def test_report_create_unauthorized(self):
        response = self.client.post('/reports/', data={
            'user': self.user.pk,
            'comment': self.c1.pk,
            'reason': 'test report'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_report_create_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/reports/', data={
            'user': self.user.pk,
            'comment': self.c1.pk,
            'reason': 'test report'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.force_authenticate(user=None)
