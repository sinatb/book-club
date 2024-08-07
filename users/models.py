from django.db import models
from django.contrib.auth.models import AbstractUser, Group
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

