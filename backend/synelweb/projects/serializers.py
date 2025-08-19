from rest_framework import serializers
from core.models import Project, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ["id", "image", "image_url", "order"]

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return ""

class ProjectSerializer(serializers.ModelSerializer):
    extra_images = ProjectImageSerializer(many=True, read_only=True)
    preview_video = serializers.FileField(allow_null=True, required=False)
    preview_image = serializers.ImageField(allow_null=True, required=False)

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