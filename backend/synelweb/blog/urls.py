from django.urls import path
from .views import BlogPostListView

urlpatterns = [
    path("blogposts/", BlogPostListView.as_view(), name="blogposts"),
]