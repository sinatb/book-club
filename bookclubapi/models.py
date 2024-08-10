from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractUser, PermissionsMixin):
    class TypeChoices(models.TextChoices):
        BASIC = 'basic', _("Basic")
        PUBLISHER = 'publisher', _("Publisher")

    user_type = models.CharField(verbose_name=_("User Type"), max_length=10, choices=TypeChoices.choices,
                                 default=TypeChoices.BASIC)
    email = models.EmailField(verbose_name=_("Email Address"), max_length=255, unique=True)

    REQUIRED_FIELDS = ['email', 'user_type']

    def is_basic(self) -> bool:
        return self.user_type == "basic"

    def is_publisher(self) -> bool:
        return self.user_type == "publisher"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Book(models.Model):
    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    publish_date = models.DateTimeField()
    like_count = models.IntegerField(default=0)
    genre = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['publish_date']

    def __str__(self) -> str:
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books_likes')

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        unique_together = ('user', 'book')

    def __str__(self) -> str:
        return f"{self.user} liked {self.book}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments')
    content = models.TextField()
    is_reported = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        unique_together = ("user", "book")
        index_together = ('user', 'book')

    def __str__(self) -> str:
        return f"{self.user} commented on {self.book}"


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        unique_together = ('user', 'comment')

    def __str__(self) -> str:
        return f"{self.user} reported {self.comment}"
