from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from bookclubapi.models import Book, Like, Comment, Report, Rating
from bookclubapi.serializers import BookSerializer, LikeSerializer, CommentSerializer, ReportSerializer, UserSerializer, \
    RatingSerializer
from .permissions import IsPublisher, IsOwner, IsCommentator
from rest_framework_simplejwt.tokens import RefreshToken


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        user_data = {
            'id': serializer.data['id'],
            'username': serializer.data['username'],
            'user_type': serializer.data['user_type'],
            'email': serializer.data['email'],
        }
        return Response(user_data)


class SignUpView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({'refresh': str(refresh),
                         'access': str(refresh.access_token),
                         }, status=status.HTTP_201_CREATED)


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsPublisher]
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE' or self.request.method == 'PUT' or self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsPublisher(), IsOwner()]
        return [permissions.AllowAny()]


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        b = get_object_or_404(Book, pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, book=b)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter(is_reported=False)
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'DELETE' or self.request.method == 'PUT' or self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCommentator()]
        return [permissions.IsAuthenticated()]


class ReportCreate(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentator]

    def perform_create(self, serializer):
        c = get_object_or_404(Comment, pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, comment=c)


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
        like_idem = Like.objects.filter(**like)
        if like_idem.exists():  # Idempotent
            return Response("Already Liked", status=status.HTTP_208_ALREADY_REPORTED)
        serializer = self.serializer_class(data=like)
        book.like_count += 1
        book.save(force_update=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        like = get_object_or_404(Like, book=book, user=request.user)
        book.like_count -= 1
        book.save(force_update=True)
        like.delete()
        return Response({'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_comment_reports(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    reports = comment.reports.all()
    serializer = CommentSerializer(reports, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_book_comments(request, pk):
    book = get_object_or_404(Book, pk=pk)
    comments = book.book_comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_book_rating(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if Rating.objects.filter(user=request.user, book=book).exists():
        return Response('Already liked', status=status.HTTP_208_ALREADY_REPORTED)
    rating = book.rating * book.rating_count + request.data.get('rating')
    book.rating_count += 1
    rating /= book.rating_count
    book.rating = rating
    book.save(force_update=True)
    rating = {
        'rating': rating
    }
    serializer = RatingSerializer(data=rating)
    if serializer.is_valid():
        serializer.save(user=request.user, book=book)
    return Response(rating, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_book_likes(request, pk):
    book = get_object_or_404(Book, pk=pk)
    likes = book.books_likes.all()
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_comment_reports(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    reports = comment.reports.all()
    serializer = CommentSerializer(reports, many=True)
    return Response(serializer.data)
