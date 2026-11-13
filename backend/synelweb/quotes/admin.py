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
    ] + ["addons_display", "languages_display"]
    exclude = ("addons", "languages")
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
