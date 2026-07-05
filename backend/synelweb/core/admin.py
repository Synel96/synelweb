from django.contrib import admin
from .models import BlogPost, BlogSection, News, NewsParagraph
from nested_admin import NestedTabularInline, NestedModelAdmin

class BlogSectionInline(admin.TabularInline):
    model = BlogSection
    extra = 1

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    inlines = [BlogSectionInline]
    list_display = ("title", "created_at")

class NewsParagraphInline(NestedTabularInline):
    model = NewsParagraph
    extra = 1

@admin.register(News)
class NewsAdmin(NestedModelAdmin):
    inlines = [NewsParagraphInline]