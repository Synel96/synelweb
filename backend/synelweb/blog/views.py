from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Article
from .serializers import ArticleDetailSerializer, ArticleListSerializer


class BlogPostListView(ListAPIView):
    queryset = Article.objects.order_by("-created_at")
    serializer_class = ArticleListSerializer


class BlogPostDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    lookup_field = "id"


class BlogPostBySlugView(BlogPostDetailView):
    """The same post, addressed by its slug (the public URL of a post)."""

    lookup_field = "slug"
