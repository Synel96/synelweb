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

    def _description_payload(self, obj):
        return self._parse_json_obj(obj.description)

    def _price_obj(self, value):
        amount = float(value) if value is not None else 0.0
        return {
            "amount": amount,
            "currency": "HUF",
        }

    def get_slug(self, obj):
        payload = self._description_payload(obj)
        if payload:
            localized = self._localized_from(payload.get("slug"))
            if localized:
                return localized
        return self._localized(obj.slug)

    def get_title(self, obj):
        payload = self._description_payload(obj)
        if payload:
            localized = self._localized_from(payload.get("title"))
            if localized:
                return localized
        return self._localized(obj.name)

    def get_description(self, obj):
        payload = self._description_payload(obj)
        if payload:
            localized = self._localized_from(payload.get("description"))
            if localized:
                return localized
        return self._localized(obj.description)

    def get_images(self, obj):
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
        payload = self._description_payload(obj)
        if payload and isinstance(payload.get("isActive"), bool):
            return payload["isActive"]
        return True

    def get_order(self, obj):
        payload = self._description_payload(obj)
        if payload and isinstance(payload.get("order"), int):
            return payload["order"]
        return obj.id