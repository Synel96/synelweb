from django.contrib import admin
from django.utils.html import format_html
from .models import Package, Review, Project, ProjectImage, BlogPost, BlogSection

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
    list_display = ("project", "image_tag", "order")
    search_fields = ("project__name",)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 100px;" />', obj.image.url)
        return "-"
    image_tag.short_description = "Kép"

class BlogSectionInline(admin.TabularInline):
    model = BlogSection
    extra = 1

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    inlines = [BlogSectionInline]
    list_display = ("title", "created_at")