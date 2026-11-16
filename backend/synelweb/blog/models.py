from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

LANGUAGES = ("hu", "en", "de")
DEFAULT_LANGUAGE = "hu"

MARKDOWN_HELP = (
    "Markdown. A „## Alcím” sorok mentén az oldal külön kártyákra bontja a szöveget; "
    "az első alcím előtti rész a bevezető."
)


class Article(models.Model):
    """A blog post: one Markdown body per language, Hungarian required.

    English and German are optional; a language left empty shows the
    Hungarian text on the site.
    """

    CATEGORY_PROFESSIONAL = "professional"
    CATEGORY_CASUAL = "casual"
    CATEGORY_DIRTY_FINANCIALS = "dirty-financials"
    CATEGORY_CHOICES = [
        (CATEGORY_PROFESSIONAL, "Szakmai"),
        (CATEGORY_CASUAL, "Hétköznapi"),
        (CATEGORY_DIRTY_FINANCIALS, "Piszkos anyagiak"),
    ]

    slug = models.SlugField(
        "URL-név",
        max_length=220,
        unique=True,
        blank=True,
        help_text=(
            "A poszt címe az URL-ben (pl. seo-eszkozok-2026). Üresen hagyva a magyar címből "
            "készül. Megjelenés után ne változtasd: a régi link megszűnik."
        ),
    )
    category = models.CharField(
        "Kategória",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_PROFESSIONAL,
        db_index=True,
    )
    preview_image = CloudinaryField("image", blank=True, null=True, help_text="Előnézeti kép")

    title_hu = models.CharField("Cím", max_length=200)
    description_hu = models.TextField(
        "Rövid leírás", blank=True, help_text="A listában és a keresőben megjelenő 1–2 mondat."
    )
    body_hu = models.TextField("Szöveg", blank=True, help_text=MARKDOWN_HELP)

    title_en = models.CharField("Title", max_length=200, blank=True)
    description_en = models.TextField("Short description", blank=True)
    body_en = models.TextField("Text", blank=True, help_text=MARKDOWN_HELP)

    title_de = models.CharField("Titel", max_length=200, blank=True)
    description_de = models.TextField("Kurzbeschreibung", blank=True)
    body_de = models.TextField("Text", blank=True, help_text=MARKDOWN_HELP)

    created_at = models.DateTimeField("Megjelenés", default=timezone.now)
    updated_at = models.DateTimeField("Utolsó módosítás", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blogposzt"
        verbose_name_plural = "Blogposztok"

    def __str__(self):
        return self.title_hu

    def is_translated(self, language):
        """A language counts as translated once it has both a title and a text."""
        if language == DEFAULT_LANGUAGE:
            return True
        title = getattr(self, f"title_{language}", "")
        body = getattr(self, f"body_{language}", "")
        return bool(title.strip() and body.strip())

    @property
    def translations(self):
        return [language for language in LANGUAGES if self.is_translated(language)]

    def language_for(self, requested):
        """The language actually served to a visitor asking for `requested`."""
        return requested if requested in LANGUAGES and self.is_translated(requested) else DEFAULT_LANGUAGE

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title_hu)[:210].strip("-") or "poszt"
            slug = base
            suffix = 1
            while type(self).objects.filter(slug=slug).exclude(pk=self.pk).exists():
                suffix += 1
                slug = f"{base}-{suffix}"
            self.slug = slug
        super().save(*args, **kwargs)
