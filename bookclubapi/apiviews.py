from rest_framework.decorators import api_view
from rest_framework import generics, permissions
from rest_framework.response import Response
from bookclubapi.models import Book
from bookclubapi.serializers import BookSerializer
from .permissions import IsPublisher


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsPublisher()]


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
def get_comment_reports(self, pk):
    return Response({})


@api_view(['GET'])
def get_book_comments(self, pk):
    return Response({})

