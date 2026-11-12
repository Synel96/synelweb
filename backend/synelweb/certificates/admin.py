from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "kind", "issuer", "issued_on", "expires_on", "order", "is_active")
    list_filter = ("category", "kind", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "issuer", "skills", "credential_id")
    fieldsets = (
        (None, {"fields": ("title", "issuer", "category", "kind", "is_active", "order")}),
        ("Dátumok", {"fields": ("issued_on", "expires_on", "hours")}),
        ("Ellenőrzés", {"fields": ("credential_url", "credential_id")}),
        ("Megjelenés", {"fields": ("skills", "badge_image_url")}),
    )
