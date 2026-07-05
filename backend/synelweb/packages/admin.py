from django.contrib import admin
from django.utils.html import format_html

from core.models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
	list_display = ("name", "image_tag", "is_discounted", "price", "discounted_price", "created_at")
	search_fields = ("name", "slug", "tags")
	list_filter = ("is_discounted", "created_at")
	prepopulated_fields = {"slug": ("name",)}

	def image_tag(self, obj):
		if obj.preview_image:
			return format_html('<img src="{}" style="max-height: 60px; max-width: 100px;" />', obj.preview_image.url)
		if obj.preview_image_url:
			return format_html('<img src="{}" style="max-height: 60px; max-width: 100px;" />', obj.preview_image_url)
		return "-"

	image_tag.short_description = "Kép"
