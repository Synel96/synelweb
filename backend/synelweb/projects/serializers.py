import json

from rest_framework import serializers
from core.models import Project, ProjectImage


DEFAULT_STACK = [
    {"name": "React", "logo": "react"},
    {"name": "TailwindCSS", "logo": "tailwind"},
    {"name": "TypeScript", "logo": "typescript"},
    {"name": "Python", "logo": "python"},
    {"name": "Django", "logo": "django"},
    {"name": "PostgreSQL", "logo": "postgresql"},
]

DEFAULT_LIGHTHOUSE = [
    {"label": "performance", "value": 100},
    {"label": "accessibility", "value": 100},
    {"label": "bestPractices", "value": 100},
    {"label": "seo", "value": 100},
]

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
    stack = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    lighthouseMobile = serializers.SerializerMethodField()
    lighthouseDesktop = serializers.SerializerMethodField()
    liveUrl = serializers.SerializerMethodField()
    isActive = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "stack",
            "description",
            "lighthouseMobile",
            "lighthouseDesktop",
            "liveUrl",
            "isActive",
            "order",
        ]

    def _localized(self, value):
        text = (value or "").strip()
        if text.startswith("{"):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict):
                    return {
                        "hu": (parsed.get("hu") or "").strip(),
                        "en": (parsed.get("en") or "").strip(),
                        "de": (parsed.get("de") or "").strip(),
                    }
            except (TypeError, ValueError, json.JSONDecodeError):
                pass
        return {
            "hu": text,
            "en": text,
            "de": text,
        }

    def get_stack(self, obj):
        return DEFAULT_STACK

    def get_description(self, obj):
        return self._localized(obj.description)

    def get_lighthouseMobile(self, obj):
        return DEFAULT_LIGHTHOUSE

    def get_lighthouseDesktop(self, obj):
        return DEFAULT_LIGHTHOUSE

    def get_liveUrl(self, obj):
        return "https://synelweb.hu"

    def get_isActive(self, obj):
        return True

    def get_order(self, obj):
        return obj.id