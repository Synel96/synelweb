from rest_framework import serializers
from core.models import BlogPost, BlogSection

class BlogSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogSection
        fields = ["id", "subtitle", "content", "order"]

class BaseBlogPostSerializer(serializers.ModelSerializer):
    sections = BlogSectionSerializer(many=True, read_only=True)
    preview_image_url = serializers.SerializerMethodField()

    def get_preview_image_url(self, obj):
        if obj.preview_image:
            # Force HTTPS for Cloudinary URLs
            url = obj.preview_image.url
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None


class BlogPostListSerializer(BaseBlogPostSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "description", "preview_image_url", "category", "created_at"]


class BlogPostDetailSerializer(BaseBlogPostSerializer):

    class Meta:
        model = BlogPost
        fields = ["id", "title", "preview_image_url", "sections", "category", "created_at"]