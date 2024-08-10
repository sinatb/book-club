from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from bookclubapi.models import Book, Like
from bookclubapi.serializers import BookSerializer, LikeSerializer
from .permissions import IsPublisher, IsOwner


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsPublisher()]


class BookDetail(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsPublisher(), IsOwner()]


class CommentCreate(generics.CreateAPIView):
    pass


class CommentDetail(generics.RetrieveDestroyAPIView):
    pass


class ReportCreate(generics.CreateAPIView):
    pass


class LikeCreate(APIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            book = get_object_or_404(Book, pk=pk)
            book.like_count += 1
            book.save(force_update=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_comment_reports(self, pk):
    return Response({})


@api_view(['GET'])
def get_book_comments(self, pk):
    return Response({})

