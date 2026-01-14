from rest_framework import serializers
from core.models import Project, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ["id", "image", "image_url", "order"]

    def get_image_url(self, obj):
        if obj.image:
            # Force HTTPS for Cloudinary URLs
            url = obj.image.url
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return ""

class ProjectSerializer(serializers.ModelSerializer):
    extra_images = ProjectImageSerializer(many=True, read_only=True)
    preview_video = serializers.SerializerMethodField()
    preview_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "slug",
            "project_type",
            "description",
            "preview_video",
            "preview_image",
            "created_at",
            "updated_at",
            "extra_images",
        ]

    def get_preview_video(self, obj):
        if obj.preview_video:
            url = obj.preview_video.url
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None

    def get_preview_image(self, obj):
        if obj.preview_image:
            url = obj.preview_image.url
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None