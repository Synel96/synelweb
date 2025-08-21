from rest_framework.generics import ListAPIView
from core.models import BlogPost
from .serializers import BlogPostSerializer



class BlogPostListView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
