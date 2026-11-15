from django.contrib import admin

from .models import SiteCheck


@admin.register(SiteCheck)
class SiteCheckAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "url",
        "strategy",
        "performance",
        "accessibility",
        "best_practices",
        "seo",
        "site_language",
    )
    list_filter = ("strategy", "site_language")
    search_fields = ("url",)
    date_hierarchy = "created_at"
    readonly_fields = [field.name for field in SiteCheck._meta.fields]

    def has_add_permission(self, request):
        return False
