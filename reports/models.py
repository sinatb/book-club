from django.db import models
from users.models import User
from comments.models import Comment
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        unique_together = ('user', 'comment')
