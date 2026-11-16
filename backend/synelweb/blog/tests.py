from unittest import mock

from django.db import connection
from django.test import SimpleTestCase, TestCase
from django.urls import resolve

from core.models import BlogPost, BlogSection

from .admin import ArticleAdminForm, extract_public_id
from .legacy_import import copy_legacy_posts
from .markdown_sections import join_sections, split_sections
from .models import Article
from .views import BlogPostBySlugView, BlogPostDetailView


class SplitSectionsTests(SimpleTestCase):
    def test_level_two_headings_start_sections(self):
        body = "Bevezető.\n\n## Első\n\nSzöveg.\n\n### Alpont\n\nMég.\n\n## Második\nVége."

        self.assertEqual(
            split_sections(body),
            [
                {"subtitle": "", "content": "Bevezető."},
                {"subtitle": "Első", "content": "Szöveg.\n\n### Alpont\n\nMég."},
                {"subtitle": "Második", "content": "Vége."},
            ],
        )

    def test_a_heading_inside_a_code_block_is_not_a_section(self):
        body = "## Kód\n\n```md\n## nem alcím\n```\n\nUtána."

        self.assertEqual(
            split_sections(body),
            [{"subtitle": "Kód", "content": "```md\n## nem alcím\n```\n\nUtána."}],
        )

    def test_empty_body_has_no_sections(self):
        self.assertEqual(split_sections(""), [])
        self.assertEqual(split_sections(None), [])

    def test_joining_and_splitting_round_trip(self):
        sections = [("Első", "Szöveg."), ("Második", "Több\n\nbekezdés.")]

        self.assertEqual(
            split_sections(join_sections(sections)),
            [{"subtitle": subtitle, "content": content} for subtitle, content in sections],
        )


class BlogUrlTests(SimpleTestCase):
    def test_numeric_address_is_an_id_and_anything_else_a_slug(self):
        by_id = resolve("/blog/blogposts/4/")
        by_slug = resolve("/blog/blogposts/seo-eszkozok-2026-ban/")

        self.assertIs(by_id.func.view_class, BlogPostDetailView)
        self.assertEqual(by_id.kwargs, {"id": 4})
        self.assertIs(by_slug.func.view_class, BlogPostBySlugView)

    def test_public_id_is_read_from_a_cloudinary_url(self):
        url = "https://res.cloudinary.com/demo/image/upload/f_auto/v123/blog/kep.webp"

        self.assertEqual(extract_public_id(url), "blog/kep")
        self.assertEqual(extract_public_id("https://example.com/kep.webp"), "")


class ArticleApiTests(TestCase):
    def setUp(self):
        self.translated = Article.objects.create(
            title_hu="Magyar cím",
            description_hu="Magyar leírás",
            body_hu="Bevezető\n\n## Rész\n\nSzöveg",
            title_en="English title",
            body_en="## Part\n\nText",
        )
        self.hungarian_only = Article.objects.create(title_hu="Csak magyar", body_hu="Szöveg")

    def get(self, path, language):
        # secure: the site redirects plain HTTP to HTTPS.
        return self.client.get(path, HTTP_ACCEPT_LANGUAGE=language, secure=True).json()

    def test_slug_comes_from_the_hungarian_title(self):
        self.assertEqual(self.translated.slug, "magyar-cim")

    def test_a_translated_post_is_served_in_the_requested_language(self):
        post = self.get(f"/blog/blogposts/{self.translated.slug}/", "en")

        self.assertEqual(post["language"], "en")
        self.assertEqual(post["title"], "English title")
        self.assertEqual(post["translations"], ["hu", "en"])
        self.assertEqual(
            post["sections"], [{"id": 1, "subtitle": "Part", "content": "Text", "order": 1}]
        )
        # No English description: the Hungarian one stands in.
        self.assertEqual(post["description"], "Magyar leírás")

    def test_an_untranslated_language_gets_the_hungarian_text(self):
        post = self.get(f"/blog/blogposts/{self.translated.id}/", "de")

        self.assertEqual(post["language"], "hu")
        self.assertEqual(post["title"], "Magyar cím")
        self.assertEqual([s["subtitle"] for s in post["sections"]], ["", "Rész"])

    def test_the_list_says_which_language_each_post_is_in(self):
        posts = {post["title"]: post for post in self.get("/blog/blogposts/", "en")}

        self.assertEqual(posts["English title"]["language"], "en")
        self.assertEqual(posts["Csak magyar"]["language"], "hu")
        self.assertEqual(posts["Csak magyar"]["translations"], ["hu"])


class ArticleAdminFormTests(TestCase):
    def form(self, **overrides):
        data = {"category": "professional", "title_hu": "Cím", "body_hu": "Szöveg", "created_at": "2026-11-16 10:00"}
        return ArticleAdminForm(data={**data, **overrides})

    def test_hungarian_alone_is_enough(self):
        self.assertTrue(self.form().is_valid())

    def test_a_translation_needs_both_title_and_text(self):
        form = self.form(title_en="Only a title")

        self.assertFalse(form.is_valid())
        self.assertIn("body_en", form.errors)


class LegacyImportTests(TestCase):
    def test_old_posts_become_articles_with_their_sections_as_markdown(self):
        old = BlogPost.objects.create(title="Régi poszt", description="Leírás", category="casual")
        BlogSection.objects.create(blog=old, subtitle="Második", content="B", order=2)
        BlogSection.objects.create(blog=old, subtitle="Első", content="A", order=1)

        self.assertEqual(copy_legacy_posts(connection, Article), 1)

        article = Article.objects.get(id=old.id)
        self.assertEqual(article.slug, old.slug)
        self.assertEqual(article.title_hu, "Régi poszt")
        self.assertEqual(article.description_hu, "Leírás")
        self.assertEqual(article.category, "casual")
        self.assertEqual(article.body_hu, "## Első\n\nA\n\n## Második\n\nB")
        self.assertEqual(article.created_at, old.created_at)
        # The old post is still there, and a second run copies nothing twice.
        self.assertTrue(BlogPost.objects.filter(id=old.id).exists())
        self.assertEqual(copy_legacy_posts(connection, Article), 0)


class DeployHookTests(TestCase):
    @mock.patch("blog.signals.trigger_vercel_deploy")
    def test_saving_a_post_rebuilds_the_site(self, mock_trigger):
        with self.captureOnCommitCallbacks(execute=True):
            Article.objects.create(title_hu="Első poszt")

        mock_trigger.assert_called_once_with("blog post created")
