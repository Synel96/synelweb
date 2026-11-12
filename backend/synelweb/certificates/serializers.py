from rest_framework import serializers

from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    issuedOn = serializers.DateField(source="issued_on")
    expiresOn = serializers.DateField(source="expires_on")
    isExpired = serializers.BooleanField(source="is_expired")
    hours = serializers.FloatField(allow_null=True)
    credentialUrl = serializers.URLField(source="credential_url")
    credentialId = serializers.CharField(source="credential_id")
    skills = serializers.ListField(source="skills_list", child=serializers.CharField())
    badgeImage = serializers.URLField(source="badge_image_url")

    class Meta:
        model = Certificate
        fields = [
            "id",
            "title",
            "issuer",
            "category",
            "kind",
            "issuedOn",
            "expiresOn",
            "isExpired",
            "hours",
            "credentialUrl",
            "credentialId",
            "skills",
            "badgeImage",
            "order",
        ]
