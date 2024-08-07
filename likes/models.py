from django.db import models
from users.models import User
from books.models import Book
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        unique_together = ('user', 'book')
