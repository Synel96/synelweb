from rest_framework.generics import ListAPIView, RetrieveAPIView
from core.models import BlogPost
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer


class BlogPostListView(ListAPIView):
    queryset = BlogPost.objects.order_by("-created_at")
    serializer_class = BlogPostListSerializer


class BlogPostDetailView(RetrieveAPIView):
    queryset = BlogPost.objects.prefetch_related("sections")
    serializer_class = BlogPostDetailSerializer
    lookup_field = "id"


class BlogPostBySlugView(BlogPostDetailView):
    """The same post, addressed by its slug (the public URL of a post)."""

    lookup_field = "slug"
