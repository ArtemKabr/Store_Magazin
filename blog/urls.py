# blog/urls.py
"""URL-маршруты приложения blog."""
from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)

app_name = "blog"

urlpatterns = [
    path("",               PostListView.as_view(),   name="post_list"),   # /blogs/
    path("create/",        PostCreateView.as_view(), name="post_create"), # /blogs/create/
    path("<int:pk>/",      PostDetailView.as_view(), name="post_detail"), # /blogs/<pk>/
    path("<int:pk>/edit/", PostUpdateView.as_view(), name="post_update"), # /blogs/<pk>/edit/
    path("<int:pk>/del/",  PostDeleteView.as_view(), name="post_delete"), # /blogs/<pk>/del/
]
