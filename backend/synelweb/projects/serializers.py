from rest_framework import serializers
from core.models import Project, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    cloudinary_public_id = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ["id", "image", "image_url", "cloudinary_public_id", "order"]

    def get_image_url(self, obj):
        if obj.image:
            # Force HTTPS for Cloudinary URLs
            url = obj.image.url
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return ""
    
    def get_cloudinary_public_id(self, obj):
        """Extract public_id from CloudinaryField"""
        if obj.image:
            return obj.image.public_id
        return ""

class ProjectSerializer(serializers.ModelSerializer):
    extra_images = ProjectImageSerializer(many=True, read_only=True)
    preview_video = serializers.SerializerMethodField()
    preview_image = serializers.SerializerMethodField()
    preview_image_public_id = serializers.SerializerMethodField()

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
            "preview_image_public_id",
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
    
    def get_preview_image_public_id(self, obj):
        """Extract public_id from preview_image CloudinaryField"""
        if obj.preview_image:
            return obj.preview_image.public_id
        return ""