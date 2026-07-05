from django.urls import path

from .views import BlogPostListView, BlogPostDetailView

urlpatterns = [
    path("blogposts/", BlogPostListView.as_view(), name="blogposts"),
    path("blogposts/<int:id>/", BlogPostDetailView.as_view(), name="blogpost-detail"),
]