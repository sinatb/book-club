from rest_framework import serializers
from .models import Book, Like, Comment, Report, User, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = []

    def create(self, validated_data):
        user = User.objects.create(
            user_type=validated_data['user_type'],
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['publisher']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ['user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user']


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        exclude = []


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['user', 'book']
