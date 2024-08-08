from django.urls import path
from .apiviews import (BookList, BookDetail, CommentCreate, CommentDetail, ReportCreate,
                       get_book_comments, get_comment_reports, CreateLike)

urlpatterns = [
    path('/books/', BookList.as_view(), 'GET all books'),
    path('/books/<int:pk>/', BookDetail.as_view(), 'GET book with id'),
    path('/comments/', CommentCreate.as_view(), 'Create a Comment'),
    path('/comments/<int:pk>/', CommentDetail.as_view(), 'DELETE or GET a comment'),
    path('/reports/', ReportCreate.as_view(), 'Create a Report'),
    path('/comments/<int:pk>/reports/', get_comment_reports, 'GET list of comment reports'),
    path('/books/<int:pk>/comments/', get_book_comments, 'GET list of comments'),
    path('/books/<int:pk>/like/', CreateLike.as_view(), 'Create a Like'),
]
