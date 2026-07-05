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

    def _parse_json_obj(self, raw_value):
        text = (raw_value or "").strip()
        if not text.startswith("{"):
            return None
        try:
            parsed = json.loads(text)
        except (TypeError, ValueError, json.JSONDecodeError):
            return None
        return parsed if isinstance(parsed, dict) else None

    def _localized_from(self, value):
        if isinstance(value, dict):
            return {
                "hu": (value.get("hu") or "").strip(),
                "en": (value.get("en") or "").strip(),
                "de": (value.get("de") or "").strip(),
            }
        return None

    def _description_payload(self, obj):
        return self._parse_json_obj(obj.description)

    def _lighthouse_array(self, value):
        if not isinstance(value, list):
            return None
        labels = {"performance", "accessibility", "bestPractices", "seo"}
        normalized = []
        for item in value:
            if not isinstance(item, dict):
                return None
            label = item.get("label")
            raw_value = item.get("value")
            if label not in labels:
                return None
            if not isinstance(raw_value, int) or raw_value < 0 or raw_value > 100:
                return None
            normalized.append({"label": label, "value": raw_value})
        if len(normalized) != 4:
            return None
        return normalized

    def _payload(self, obj):
        return self._description_payload(obj) or {}

    def _localized(self, value):
        if isinstance(value, dict):
            return {
                "hu": (value.get("hu") or "").strip(),
                "en": (value.get("en") or "").strip(),
                "de": (value.get("de") or "").strip(),
            }
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
        payload = self._payload(obj)
        stack = payload.get("stack")
        if isinstance(stack, list) and stack:
            return stack
        return DEFAULT_STACK

    def get_description(self, obj):
        payload = self._payload(obj)
        description = payload.get("description")
        if description is not None:
            return self._localized(description)
        return self._localized(obj.description)

    def get_lighthouseMobile(self, obj):
        payload = self._payload(obj)
        lighthouse_mobile = self._lighthouse_array(payload.get("lighthouseMobile"))
        if lighthouse_mobile:
            return lighthouse_mobile
        return DEFAULT_LIGHTHOUSE

    def get_lighthouseDesktop(self, obj):
        payload = self._payload(obj)
        lighthouse_desktop = self._lighthouse_array(payload.get("lighthouseDesktop"))
        if lighthouse_desktop:
            return lighthouse_desktop
        return DEFAULT_LIGHTHOUSE

    def get_liveUrl(self, obj):
        payload = self._payload(obj)
        live_url = payload.get("liveUrl")
        if isinstance(live_url, str) and live_url.strip():
            return live_url.strip()
        return "https://synelweb.hu"

    def get_isActive(self, obj):
        payload = self._payload(obj)
        is_active = payload.get("isActive")
        if isinstance(is_active, bool):
            return is_active
        return True

    def get_order(self, obj):
        payload = self._payload(obj)
        order = payload.get("order")
        if isinstance(order, int):
            return order
        return obj.id