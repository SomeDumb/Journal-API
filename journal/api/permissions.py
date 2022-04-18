from rest_framework import permissions
from .models import Article, JournalUser
from django.contrib.auth.models import Group

class IsAuthorOrReadOnly(permissions.BasePermission):
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return str(obj.author) == request.user.email

class IsAuthor(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.has_perm('api.can_create_article')