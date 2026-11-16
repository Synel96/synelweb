from django.urls import path

from .views import BlogPostBySlugView, BlogPostDetailView, BlogPostListView

urlpatterns = [
    path("blogposts/", BlogPostListView.as_view(), name="blogposts"),
    # A numeric id keeps working (old links); anything else is a slug.
    path("blogposts/<int:id>/", BlogPostDetailView.as_view(), name="blogpost-detail"),
    path("blogposts/<slug:slug>/", BlogPostBySlugView.as_view(), name="blogpost-by-slug"),
]
