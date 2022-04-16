from rest_framework import permissions, status, exceptions, filters
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .permissions import IsAuthorOrReadOnly
from .serializers import UserSerializer, ArticleSerializer
from .models import Article, JournalUser

class CreateUserView(CreateAPIView):

    model = JournalUser
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
class UserList(APIView):

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        emails = [user.email for user in JournalUser.objects.all()]
        return Response(emails)

def permission_required(permission_name, raise_exception=False):
    class PermissionRequired(permissions.BasePermission):
        def has_permission(self, request, view):
            if not request.user.has_perm(permission_name):
                if raise_exception:
                    raise exceptions.PermissionDenied("Don't have permission")
                return False
            return True
    return PermissionRequired

class ArticleList(ListAPIView):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'author']
    serializer_class = ArticleSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            articles=Article.objects.all()
        else:
            articles=Article.objects.filter(for_subscribers=False)
        return articles

class ArticleDetailView(APIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly]
    
    def put(self, request, pk, format=None):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pass
        
    def get(self, request, pk, format=None):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)