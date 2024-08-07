from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


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
