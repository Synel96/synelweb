from django.contrib import admin
from django.utils.html import format_html

from core.models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
	model = ProjectImage
	extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ("name", "project_type", "preview_tag", "created_at")
	search_fields = ("name", "slug", "project_type")
	prepopulated_fields = {"slug": ("name",)}
	inlines = [ProjectImageInline]

	def preview_tag(self, obj):
		if obj.preview_image:
			return format_html('<img src="{}" style="max-height: 60px; max-width: 100px;" />', obj.preview_image.url)
		return "-"

	preview_tag.short_description = "Előnézet"


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
	list_display = ("project", "image_tag", "order")
	search_fields = ("project__name",)
	list_filter = ("project",)

	def image_tag(self, obj):
		if obj.image:
			return format_html('<img src="{}" style="max-height: 60px; max-width: 100px;" />', obj.image.url)
		return "-"

	image_tag.short_description = "Kép"
