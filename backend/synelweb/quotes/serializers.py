from rest_framework import serializers

from .models import QuoteRequest


class QuoteRequestSerializer(serializers.ModelSerializer):
    """Accepts the contact page's quote form (camelCase, like the other APIs).

    `company` is a honeypot: hidden from people, so only bots fill it in.
    """

    existingSite = serializers.ChoiceField(
        source="existing_site",
        choices=QuoteRequest.ExistingSite.choices,
        required=False,
        allow_blank=True,
    )
    websiteUrl = serializers.CharField(
        source="website_url", required=False, allow_blank=True, max_length=300
    )
    isLocal = serializers.BooleanField(source="is_local", required=False)
    isGrantFunded = serializers.BooleanField(source="is_grant_funded", required=False)
    contactPreference = serializers.ChoiceField(
        source="contact_preference",
        choices=QuoteRequest.ContactPreference.choices,
        required=False,
        allow_blank=True,
    )
    siteLanguage = serializers.ChoiceField(
        source="site_language", choices=["hu", "en", "de"], required=False
    )
    languages = serializers.ListField(
        child=serializers.ChoiceField(choices=list(QuoteRequest.LANGUAGES)),
        required=False,
        max_length=3,
    )
    addons = serializers.ListField(
        child=serializers.ChoiceField(choices=list(QuoteRequest.ADDONS)),
        required=False,
        max_length=len(QuoteRequest.ADDONS),
    )
    company = serializers.CharField(required=False, allow_blank=True, write_only=True)

    DETAILED_ONLY = (
        "existing_site",
        "website_url",
        "size",
        "languages",
        "addons",
        "timeline",
        "budget",
        "is_local",
        "is_grant_funded",
        "contact_preference",
    )

    class Meta:
        model = QuoteRequest
        fields = [
            "mode",
            "service",
            "name",
            "email",
            "phone",
            "message",
            "existingSite",
            "websiteUrl",
            "size",
            "languages",
            "addons",
            "timeline",
            "budget",
            "isLocal",
            "isGrantFunded",
            "contactPreference",
            "siteLanguage",
            "consent",
            "company",
        ]
        extra_kwargs = {
            "name": {"min_length": 2},
            "message": {"min_length": 10},
            "phone": {"required": False},
            "consent": {"required": True},
        }

    def validate_consent(self, value):
        if value is not True:
            raise serializers.ValidationError("Consent to the privacy notice is required.")
        return value

    def validate(self, attrs):
        attrs.pop("company", None)
        if attrs.get("mode") == QuoteRequest.Mode.SIMPLE:
            # A simplified request carries no detail fields, whatever the
            # client sent (e.g. values left over from the detailed tab).
            for field in self.DETAILED_ONLY:
                attrs.pop(field, None)
        for field in ("languages", "addons"):
            if field in attrs:
                attrs[field] = list(dict.fromkeys(attrs[field]))
        return attrs
