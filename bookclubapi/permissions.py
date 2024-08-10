from rest_framework import permissions


class IsPublisher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'publisher'


class IsCommentator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.pk == request.user.pk


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.publisher.pk == request.user.pk
