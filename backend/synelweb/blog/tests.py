from django.test import SimpleTestCase
from django.urls import resolve

from .serializers import BlogPostDetailSerializer, BlogPostListSerializer
from .views import BlogPostBySlugView, BlogPostDetailView


class BlogApiShapeTests(SimpleTestCase):
    def test_numeric_address_is_an_id_and_anything_else_a_slug(self):
        by_id = resolve("/blog/blogposts/4/")
        by_slug = resolve("/blog/blogposts/seo-eszkozok-2026-ban/")

        self.assertIs(by_id.func.view_class, BlogPostDetailView)
        self.assertEqual(by_id.kwargs, {"id": 4})
        self.assertIs(by_slug.func.view_class, BlogPostBySlugView)
        self.assertEqual(by_slug.kwargs, {"slug": "seo-eszkozok-2026-ban"})

    def test_posts_expose_slug_and_modification_date(self):
        for serializer in (BlogPostListSerializer, BlogPostDetailSerializer):
            fields = serializer.Meta.fields
            self.assertIn("slug", fields)
            self.assertIn("updated_at", fields)
            self.assertIn("description", fields)
