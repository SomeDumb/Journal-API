from django.contrib import admin
from django.urls import path

from .views import CreateUserView, UserList, \
    ArticleList, ArticleDetailView
    
urlpatterns = [
    path('register', CreateUserView.as_view(),),
    path('users', UserList.as_view(),),
    path('articles', ArticleList.as_view(),),
    path('article/<int:pk>/', ArticleDetailView.as_view(),),
]