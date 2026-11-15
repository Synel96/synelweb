from urllib.parse import urlsplit

from rest_framework import serializers

from .models import SiteCheck


class SiteCheckRequestSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=500)
    strategy = serializers.ChoiceField(choices=SiteCheck.Strategy.choices, default="mobile")
    lang = serializers.ChoiceField(choices=["hu", "en", "de"], default="hu")

    def validate_url(self, value):
        value = value.strip()
        if "://" not in value:
            value = f"https://{value}"
        parts = urlsplit(value)
        host = (parts.hostname or "").lower()
        if parts.scheme not in ("http", "https") or "." not in host or " " in value:
            raise serializers.ValidationError("Enter a website address, e.g. pelda.hu.")
        if host in ("localhost",) or host.endswith(".local") or host.replace(".", "").isdigit():
            raise serializers.ValidationError("Only public websites can be checked.")
        return value
