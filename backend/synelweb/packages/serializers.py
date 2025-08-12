from rest_framework import serializers
from core.models import Package

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = [
            "id",
            "name",
            "slug",
            "preview_image_url",
            "description",
            "is_discounted",
            "tags",
            "created_at",
            "updated_at",
        ]