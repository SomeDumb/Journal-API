from rest_framework import permissions, status, exceptions, filters
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from .permissions import IsAuthorOrReadOnly, IsAuthor
from .serializers import UserSerializer, ArticleSerializer
from .models import Article, JournalUser

class CreateUserView(CreateAPIView):
    """
    Creates JournalUser object and adds it to the subscriber group.
    """
    model = JournalUser
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    
class UserList(APIView):
    """
    Shows list of existing users in model JournalUser if requested from admin.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        emails = [user.email for user in JournalUser.objects.all()]
        return Response(emails)

class ArticleList(ListAPIView):
    """
    Shows list of Articles based on users premissions.
    """
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
    """
    Shows Article  based on users premissions.
    Allows put and delete requests if user is author.
    """
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly,]
    
    def put(self, request, pk, format=None):
        article = get_object_or_404(Article, pk=pk)
        article.changed_at=now()
        self.check_object_permissions(self.request, article)
        serializer = ArticleSerializer(article, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article = get_object_or_404(Article, pk=pk)
        self.check_object_permissions(self.request, article)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    def get(self, request, pk, format=None):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        if not request.user.has_perm('api.can_view_article') and article.for_subscribers:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.data)
    
class NewArticleView(CreateAPIView):
    """
    Creates new Article if user has permission.
    """
    model = Article
    permission_classes = [IsAuthor]
    serializer_class = ArticleSerializer
    
    def perform_create(self, serializer):
        author = get_object_or_404(JournalUser, id=self.request.user.id)
        return serializer.save(author=author)