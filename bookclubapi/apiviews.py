from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Book


class BookListAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    pass


class BookDetailAPIView(APIView):

    def get(self, request, pk):
        return Response({})

    def delete(self, request, pk):
        return Response({})


class CommentListAPIView(APIView):

    def post(self, request, pk):
        return Response({})


class CommentDetailAPIView(APIView):

    def get(self, request, pk):
        return Response({})

    def delete(self, request, pk):
        return Response({})


class ReporterListAPIView(APIView):

    def post(self, request):
        return Response({})


class CommentsReportListAPIView(APIView):
    def get(self, request, pk):
        return Response({})


class BooksCommentListAPIView(APIView):

    def get(self, request, pk):
        return Response({})

