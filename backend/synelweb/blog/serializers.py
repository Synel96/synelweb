from rest_framework import serializers

from .markdown_sections import split_sections
from .models import DEFAULT_LANGUAGE, LANGUAGES, Article


def requested_language(request):
    """The site language of the request (the frontend sends Accept-Language)."""
    header = (request.headers.get("Accept-Language", "") if request else "").lower()
    code = header.split(",")[0].strip()[:2]
    return code if code in LANGUAGES else DEFAULT_LANGUAGE


class ArticleListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    preview_image_url = serializers.SerializerMethodField()
    # The language the texts below are in: the requested one when the post is
    # translated into it, Hungarian otherwise.
    language = serializers.SerializerMethodField()
    translations = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "preview_image_url",
            "category",
            "language",
            "translations",
            "created_at",
            "updated_at",
        ]

    def get_language(self, obj):
        return obj.language_for(requested_language(self.context.get("request")))

    def _text(self, obj, field):
        return getattr(obj, f"{field}_{self.get_language(obj)}")

    def get_title(self, obj):
        return self._text(obj, "title")

    def get_description(self, obj):
        # A translated post without its own description falls back to the
        # Hungarian one rather than showing nothing.
        return self._text(obj, "description") or obj.description_hu

    def get_preview_image_url(self, obj):
        if not obj.preview_image:
            return None
        url = obj.preview_image.url
        return url.replace("http://", "https://", 1) if url.startswith("http://") else url


class ArticleDetailSerializer(ArticleListSerializer):
    body = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()

    class Meta(ArticleListSerializer.Meta):
        fields = ArticleListSerializer.Meta.fields + ["body", "sections"]

    def get_body(self, obj):
        return self._text(obj, "body")

    def get_sections(self, obj):
        return [
            {"id": index, "subtitle": section["subtitle"], "content": section["content"], "order": index}
            for index, section in enumerate(split_sections(self.get_body(obj)), start=1)
        ]
