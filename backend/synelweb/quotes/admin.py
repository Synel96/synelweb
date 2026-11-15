from django.contrib import admin

from .models import QuoteRequest


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "service_column", "mode", "budget", "status")
    list_filter = ("status", "mode", "service", "budget", "is_local", "is_grant_funded")
    search_fields = ("name", "email", "phone", "message", "website_url")
    list_editable = ("status",)
    date_hierarchy = "created_at"
    readonly_fields = [
        field.name for field in QuoteRequest._meta.fields if field.name not in ("id", "status")
    ] + ["addons_display", "languages_display", "site_check_display"]
    exclude = ("addons", "languages", "site_check")
    fieldsets = (
        (None, {"fields": ("status", "mode", "created_at", "site_language")}),
        ("Kapcsolat", {"fields": ("name", "email", "phone", "contact_preference")}),
        ("Kérés", {"fields": ("service_name", "service", "message")}),
        (
            "Részletek",
            {
                "fields": (
                    "existing_site",
                    "website_url",
                    "domain",
                    "domain_name",
                    "size",
                    "languages_display",
                    "addons_display",
                    "timeline",
                    "budget",
                    "ads_account",
                    "ad_budget",
                    "is_local",
                    "is_grant_funded",
                )
            },
        ),
        ("Weboldal-ellenőrzés", {"fields": ("site_check_display",)}),
        ("Adatkezelés", {"fields": ("consent",)}),
    )

    @admin.display(description="Szolgáltatás", ordering="service_name")
    def service_column(self, obj):
        return obj.service_display()

    @admin.display(description="Kiegészítők")
    def addons_display(self, obj):
        return ", ".join(obj.addon_labels()) or "-"

    @admin.display(description="Nyelvek")
    def languages_display(self, obj):
        return ", ".join(obj.language_labels()) or "-"

    def has_add_permission(self, request):
        return False

    @admin.display(description="Csatolt weboldal-ellenőrzés")
    def site_check_display(self, obj):
        from django.utils.html import format_html
        from .notifications import _site_check_lines

        if not obj.site_check:
            return "–"
        return format_html(
            "<pre style='white-space:pre-wrap;margin:0'>{}</pre>",
            "\n".join(_site_check_lines(obj.site_check)),
        )
