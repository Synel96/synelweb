from rest_framework import serializers
from core.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "name",
            "email",
            "rating",
            "comment",
            "created_at",
        ]