from django.urls import path
from .apiviews import (BookList, BookDetail, CommentCreate, CommentDetail, ReportCreate,
                       get_book_comments, get_comment_reports, CreateLike)

urlpatterns = [
    path('books/', BookList.as_view(), name='get_book_list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='get_book_detail'),
    path('comments/', CommentCreate.as_view(), name='create_comment'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='get_comment_detail'),
    path('reports/', ReportCreate.as_view(), name='create_report'),
    path('comments/<int:pk>/reports/', get_comment_reports, name='get_comment_reports'),
    path('books/<int:pk>/comments/', get_book_comments, name='get_book_comments'),
    path('books/<int:pk>/like/', CreateLike.as_view(), name='create_like'),
]
