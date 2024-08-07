from django.db import models
from users.models import User
from books.models import Book
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    is_reported = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        unique_together = ("user", "book")
