from urllib.parse import urlparse

from django import forms
from django.contrib import admin, messages

from .markdown_sections import split_sections
from .models import Article


def extract_public_id(cloudinary_url):
    """The Cloudinary public id inside an image URL ('' if there is none).

    /upload/<transformations>/v<version>/<public_id>.<ext>
    """
    path = urlparse(cloudinary_url).path or ""
    if "/upload/" not in path:
        return ""
    tail = path.split("/upload/", 1)[1].split("?", 1)[0].strip("/")
    parts = [part for part in tail.split("/") if part]

    version_index = next(
        (index for index, part in enumerate(parts) if part.startswith("v") and part[1:].isdigit()),
        None,
    )
    if version_index is not None:
        parts = parts[version_index + 1 :]
    if not parts:
        return ""

    parts[-1] = parts[-1].rsplit(".", 1)[0] if "." in parts[-1] else parts[-1]
    return "/".join(parts)


class ArticleAdminForm(forms.ModelForm):
    preview_image_link = forms.URLField(
        required=False,
        label="Előnézeti kép Cloudinary URL-je",
        help_text=(
            "Egy már feltöltött Cloudinary kép címe, pl. "
            "https://res.cloudinary.com/<cloud>/image/upload/v123/mappa/kep.webp"
        ),
    )

    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            **{
                f"body_{language}": forms.Textarea(attrs={"rows": 28, "style": "width: 95%; font-family: monospace;"})
                for language in ("hu", "en", "de")
            },
            **{
                f"description_{language}": forms.Textarea(attrs={"rows": 3, "style": "width: 95%;"})
                for language in ("hu", "en", "de")
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.preview_image:
            self.fields["preview_image_link"].initial = self.instance.preview_image.url

    def clean_preview_image_link(self):
        value = (self.cleaned_data.get("preview_image_link") or "").strip()
        if not value:
            return ""
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise forms.ValidationError("Érvénytelen URL.")
        if "/image/upload/" not in parsed.path:
            raise forms.ValidationError("Csak Cloudinary képcím használható (/image/upload/).")
        return value

    def clean(self):
        cleaned = super().clean()
        # A half-filled translation would silently show the Hungarian text.
        for language, name in (("en", "angol"), ("de", "német")):
            title = (cleaned.get(f"title_{language}") or "").strip()
            body = (cleaned.get(f"body_{language}") or "").strip()
            if bool(title) != bool(body):
                missing = f"title_{language}" if not title else f"body_{language}"
                self.add_error(
                    missing,
                    f"Az {name} fordításhoz cím és szöveg is kell – töltsd ki ezt is, "
                    "vagy hagyd mindkettőt üresen.",
                )
        return cleaned


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ("title_hu", "category", "languages", "section_count", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title_hu", "title_en", "title_de", "description_hu", "body_hu")
    readonly_fields = ("updated_at",)
    fieldsets = (
        (None, {"fields": ("category", "preview_image_link", "preview_image", "slug", "created_at", "updated_at")}),
        ("Magyar", {"fields": ("title_hu", "description_hu", "body_hu")}),
        (
            "English (nem kötelező)",
            {
                "classes": ("collapse",),
                "description": "Üresen hagyva az angol oldalon a magyar szöveg jelenik meg.",
                "fields": ("title_en", "description_en", "body_en"),
            },
        ),
        (
            "Deutsch (nem kötelező)",
            {
                "classes": ("collapse",),
                "description": "Üresen hagyva a német oldalon a magyar szöveg jelenik meg.",
                "fields": ("title_de", "description_de", "body_de"),
            },
        ),
    )

    @admin.display(description="Nyelvek")
    def languages(self, obj):
        return ", ".join(language.upper() for language in obj.translations)

    @admin.display(description="Szekciók (HU)")
    def section_count(self, obj):
        return len(split_sections(obj.body_hu))

    def save_model(self, request, obj, form, change):
        link = form.cleaned_data.get("preview_image_link")
        if link:
            public_id = extract_public_id(link)
            if public_id:
                obj.preview_image = public_id
            else:
                messages.warning(
                    request, "A Cloudinary címből nem sikerült kiolvasni a képet, az előnézeti kép nem változott."
                )
        super().save_model(request, obj, form, change)
