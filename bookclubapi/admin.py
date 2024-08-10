from django.contrib import admin
from .models import User, Book, Report, Comment, Like
# Register your models here.

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Report)
admin.site.register(Comment)
admin.site.register(Like)