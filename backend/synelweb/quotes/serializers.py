import json

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
    serviceName = serializers.CharField(
        source="service_name", required=False, allow_blank=True, max_length=200
    )
    domainName = serializers.CharField(
        source="domain_name", required=False, allow_blank=True, max_length=253
    )
    adsAccount = serializers.ChoiceField(
        source="ads_account",
        choices=QuoteRequest.AdsAccount.choices,
        required=False,
        allow_blank=True,
    )
    adBudget = serializers.ChoiceField(
        source="ad_budget",
        choices=QuoteRequest.AdBudget.choices,
        required=False,
        allow_blank=True,
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
    siteCheck = serializers.JSONField(source="site_check", required=False, allow_null=True)
    company = serializers.CharField(required=False, allow_blank=True, write_only=True)

    DETAILED_ONLY = (
        "existing_site",
        "website_url",
        "domain",
        "domain_name",
        "size",
        "languages",
        "addons",
        "timeline",
        "budget",
        "ads_account",
        "ad_budget",
        "is_local",
        "is_grant_funded",
    )

    class Meta:
        model = QuoteRequest
        fields = [
            "mode",
            "service",
            "serviceName",
            "name",
            "email",
            "phone",
            "message",
            "existingSite",
            "websiteUrl",
            "domain",
            "domainName",
            "size",
            "languages",
            "addons",
            "timeline",
            "budget",
            "adsAccount",
            "adBudget",
            "isLocal",
            "isGrantFunded",
            "contactPreference",
            "siteLanguage",
            "siteCheck",
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

    SITE_CHECK_MAX_CHARS = 10_000

    def validate_siteCheck(self, value):
        """A website check from the site's checker: a small JSON object."""
        if value is None:
            return None
        if not isinstance(value, dict) or not isinstance(value.get("url"), str):
            raise serializers.ValidationError("Invalid website check.")
        if len(json.dumps(value)) > self.SITE_CHECK_MAX_CHARS:
            raise serializers.ValidationError("Website check too large.")
        return value

    def validate(self, attrs):
        attrs.pop("company", None)
        if attrs.get("mode") == QuoteRequest.Mode.SIMPLE:
            # A simplified request carries no detail fields, whatever the
            # client sent (e.g. values left over from the detailed tab),
            # except the ads add-on: asking for ads with the website is a
            # choice of the simple form too (the bundle offer).
            wants_bundle = QuoteRequest.BUNDLE_ADDON in attrs.get("addons", [])
            for field in self.DETAILED_ONLY:
                attrs.pop(field, None)
            if wants_bundle:
                attrs["addons"] = [QuoteRequest.BUNDLE_ADDON]
        if attrs.get("domain") != QuoteRequest.Domain.HAS:
            attrs.pop("domain_name", None)
        for field in ("languages", "addons"):
            if field in attrs:
                attrs[field] = list(dict.fromkeys(attrs[field]))
        return attrs
