from rest_framework import serializers
from core.models import BlogPost, BlogSection

class BlogSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogSection
        fields = ["id", "subtitle", "content", "order"]

class BlogPostSerializer(serializers.ModelSerializer):
    sections = BlogSectionSerializer(many=True, read_only=True)
    preview_image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "preview_image_url",
            "created_at",
            "updated_at",
            "sections",
        ]

    def get_preview_image_url(self, obj):
        if obj.preview_image:
            return obj.preview_image.url