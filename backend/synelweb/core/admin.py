from django.contrib import admin
from .models import Package, Review, Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "is_discounted", "created_at")
    search_fields = ("name", "tags")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "created_at")
    search_fields = ("name", "comment")

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "image_url", "order")
    search_fields = ("image_url",)