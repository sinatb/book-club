from django.urls import path
from .apiviews import (BookList, BookDetail, CommentCreate, CommentDetail, ReportCreate,
                       get_book_comments, get_comment_reports, LikeCreate, SignUpView, post_book_rating,
                       UserView, BookCreateView, get_book_likes)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
urlpatterns = [

    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user_apis'),
    path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('books/', BookList.as_view(), name='get_book_list'),
    path('book/', BookCreateView.as_view(), name='create_book'),
    path('books/<int:pk>/', BookDetail.as_view(), name='get_book_detail'),
    path('books/<int:pk>/comment/', CommentCreate.as_view(), name='create_comment'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='get_comment_detail'),
    path('comments/<int:pk>/report/', ReportCreate.as_view(), name='create_report'),
    path('comments/<int:pk>/reports/', get_comment_reports, name='get_comment_reports'),
    path('books/<int:pk>/comments/', get_book_comments, name='get_book_comments'),
    path('books/<int:pk>/like/', LikeCreate.as_view(), name='create_like'),
    path('books/<int:pk>/rate/', post_book_rating, name="rate_book"),
    path('books/<int:pk>/likes/', get_book_likes, name='get_book_likes'),
]
