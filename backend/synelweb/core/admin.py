from urllib.parse import urlparse

from django import forms
from django.contrib import admin, messages

from .models import BlogPost, BlogSection, News, NewsParagraph
from nested_admin import NestedTabularInline, NestedModelAdmin

class BlogSectionInline(admin.TabularInline):
    model = BlogSection
    extra = 1


class BlogPostAdminForm(forms.ModelForm):
    preview_image_link = forms.URLField(
        required=False,
        help_text=(
            "Cloudinary image URL (upload tipus), pl.: "
            "https://res.cloudinary.com/<cloud>/image/upload/v123/folder/kep.webp"
        ),
        label="Preview image Cloudinary URL",
    )

    class Meta:
        model = BlogPost
        fields = "__all__"

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
            raise forms.ValidationError("Ervenytelen URL.")

        if "/image/upload/" not in parsed.path:
            raise forms.ValidationError(
                "Csak Cloudinary upload kep URL tamogatott (/image/upload/)."
            )

        return value

    @staticmethod
    def extract_public_id(cloudinary_url: str) -> str:
        parsed = urlparse(cloudinary_url)
        path = parsed.path or ""

        _, tail = path.split("/upload/", 1)
        tail = tail.split("?", 1)[0].strip("/")
        parts = [part for part in tail.split("/") if part]

        # /upload/<transformok>/v<verzio>/<public_id>.<ext>
        version_index = next(
            (idx for idx, part in enumerate(parts) if part.startswith("v") and part[1:].isdigit()),
            None,
        )
        if version_index is not None:
            parts = parts[version_index + 1 :]

        if not parts:
            return ""

        last = parts[-1]
        if "." in last:
            last = last.rsplit(".", 1)[0]
        parts[-1] = last
        return "/".join(parts)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    inlines = [BlogSectionInline]
    list_display = ("title", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        preview_image_link = form.cleaned_data.get("preview_image_link")
        if preview_image_link:
            public_id = form.extract_public_id(preview_image_link)
            if public_id:
                obj.preview_image = public_id
            else:
                messages.warning(
                    request,
                    "A Cloudinary URL-bol nem sikerult public_id-t kinyerni, a kep nem frissult.",
                )

        super().save_model(request, obj, form, change)

class NewsParagraphInline(NestedTabularInline):
    model = NewsParagraph
    extra = 1

@admin.register(News)
class NewsAdmin(NestedModelAdmin):
    inlines = [NewsParagraphInline]