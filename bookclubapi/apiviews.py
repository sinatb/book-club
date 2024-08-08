from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.response import Response
from .models import Book


class BookList(generics.ListCreateAPIView):
    pass


class BookDetail(generics.RetrieveDestroyAPIView):
    pass


class CommentCreate(generics.CreateAPIView):
    pass


class CommentDetail(generics.RetrieveDestroyAPIView):
    pass


class ReportCreate(generics.CreateAPIView):
    pass


class CreateLike(generics.CreateAPIView):
    pass


@api_view(['GET'])
def get_comment_reports(self, request, pk):
    return Response({})


@api_view(['GET'])
def get_book_comments(self, request, pk):
    return Response({})

