from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import CreateUserView, UserList, \
    ArticleList, ArticleDetailView, NewArticleView
    
urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('register/', CreateUserView.as_view(),),
    path('users/', UserList.as_view(),),
    path('articles/', ArticleList.as_view(),),
    path('article/<int:pk>/', ArticleDetailView.as_view(),),
    
    path('new_article/', NewArticleView.as_view(),),
]