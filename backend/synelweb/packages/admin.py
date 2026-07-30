from django.contrib import admin

from .models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("target_currency", "rate", "updated_at")
    readonly_fields = ("updated_at",)
