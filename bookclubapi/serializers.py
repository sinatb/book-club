from rest_framework import serializers
from .models import Book, Like, Comment, Report


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = []


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ['user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = []


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = []
