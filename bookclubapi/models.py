from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):

    USER_TYPE_CHOICES = (
        ("basic", "Basic"),
        ("publisher", "Publisher")
    )

    user_type = models.CharField(_("User Type"), max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(_("Email Address"), max_length=255, unique=True)

    REQUIRED_FIELDS = ['email', 'user_type']

    def is_basic(self):
        return self.user_type == "basic"

    def is_publisher(self):
        return self.user_type == "publisher"

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Book(models.Model):

    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    rating_count = models.IntegerField()
    publish_date = models.DateTimeField()
    like_count = models.IntegerField()
    Genre = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.name


class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        unique_together = ('user', 'book')


class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    is_reported = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        unique_together = ("user", "book")


class Report(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        unique_together = ('user', 'comment')
