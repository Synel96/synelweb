import json

from rest_framework import serializers
from core.models import Package


class PackageSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    salePrice = serializers.SerializerMethodField()
    isActive = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "images",
            "price",
            "salePrice",
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

    def _price_obj(self, value):
        amount = float(value) if value is not None else 0.0
        return {
            "amount": amount,
            "currency": "HUF",
        }

    def get_slug(self, obj):
        return self._localized(obj.slug)

    def get_title(self, obj):
        return self._localized(obj.name)

    def get_description(self, obj):
        return self._localized(obj.description)

    def get_images(self, obj):
        if obj.preview_image:
            url = obj.preview_image.url
            if url.startswith("http://"):
                url = url.replace("http://", "https://", 1)
            return [url]
        if obj.preview_image_url:
            return [obj.preview_image_url]
        return []

    def get_price(self, obj):
        return self._price_obj(obj.price)

    def get_salePrice(self, obj):
        if obj.is_discounted and obj.discounted_price is not None:
            return self._price_obj(obj.discounted_price)
        return None

    def get_isActive(self, obj):
        return True

    def get_order(self, obj):
        return obj.id