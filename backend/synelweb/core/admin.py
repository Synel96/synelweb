from urllib.parse import urlparse

from django import forms
from django.contrib import admin, messages

from .models import News, NewsParagraph
from nested_admin import NestedTabularInline, NestedModelAdmin

# Blog posts are managed in the blog app (blog.Article); the old BlogPost /
# BlogSection tables are kept untouched as the pre-migration backup.

class NewsParagraphInline(NestedTabularInline):
    model = NewsParagraph
    extra = 1

@admin.register(News)
class NewsAdmin(NestedModelAdmin):
    inlines = [NewsParagraphInline]