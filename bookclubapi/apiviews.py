from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from bookclubapi.models import Book, Like, Comment, Report
from bookclubapi.serializers import BookSerializer, LikeSerializer, CommentSerializer, ReportSerializer
from .permissions import IsPublisher, IsOwner, IsCommentator


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsPublisher()]


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'DELETE' or self.request.method == 'PUT':
            return [permissions.IsAuthenticated(), IsPublisher(), IsOwner()]


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentator]


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter(is_reported=False)
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE' or self.request.method == 'PUT':
            return [permissions.IsAuthenticated(), IsCommentator()]
        else:
            return [permissions.IsAuthenticated()]


class ReportCreate(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentator]


class LikeCreate(APIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        like = {
            'user': request.user.pk,
            'book': book.pk,
        }
        serializer = self.serializer_class(data=like)
        book.like_count += 1
        book.save(force_update=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        print(Like.objects.values())
        print(book.name)
        print(request.user)
        like = get_object_or_404(Like, book=book, user=request.user)
        book.like_count -= 1
        book.save(force_update=True)
        like.delete()
        return Response({'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_comment_reports(self, pk):
    comment = get_object_or_404(Comment, pk=pk)
    reports = comment.reports.all()
    serializer = CommentSerializer(reports, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_book_comments(self, pk):
    book = get_object_or_404(Book, pk=pk)
    comments = book.book_comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
