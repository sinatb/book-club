import datetime

from rest_framework import status
from rest_framework.test import APIClient
from bookclubapi.models import Book, Comment
from bookclubapi.serializers import BookSerializer
from .testbase import BookClubTestBase

# Create your tests here.
client = APIClient()


class ReportAPITests(BookClubTestBase):
    def setUp(self):
        pass