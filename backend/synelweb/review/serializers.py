from rest_framework import serializers
from core.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    review = serializers.CharField(source="comment", required=False, allow_blank=True)
    isApproved = serializers.BooleanField(source="is_approved", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "name",
            "email",
            "rating",
            "review",
            "isApproved",
            "createdAt",
        ]
        extra_kwargs = {
            "name": {"min_length": 2},
            "email": {"required": True, "allow_null": False, "allow_blank": False},
        }

    def validate_rating(self, value):
        if int(value) != value:
            raise serializers.ValidationError("Rating must be an integer between 0 and 5.")
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value

    def validate(self, attrs):
        comment = attrs.get("comment")

        # Backward compatibility: allow incoming `comment` key.
        if not comment:
            raw_comment = self.initial_data.get("comment", "")
            if raw_comment:
                attrs["comment"] = raw_comment
                comment = raw_comment

        if not comment or len(comment.strip()) < 10:
            raise serializers.ValidationError({
                "review": "Review must be at least 10 characters long."
            })

        return attrs

    def create(self, validated_data):
        validated_data["is_approved"] = False
        return super().create(validated_data)