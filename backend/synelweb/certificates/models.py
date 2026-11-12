from django.db import models
from django.utils import timezone


class Certificate(models.Model):
    """A certificate shown on the site's Certificates page."""

    class Category(models.TextChoices):
        FRONTEND = "frontend", "Frontend webfejlesztés"
        BACKEND = "backend", "Backend"
        FULLSTACK = "fullstack", "Fullstack"
        MARKETING = "marketing", "Search Ads és marketing"

    class Kind(models.TextChoices):
        EXAM = "exam", "Vizsgával szerzett tanúsítvány"
        COURSE = "course", "Elvégzett kurzus"

    title = models.CharField("Megnevezés", max_length=200)
    issuer = models.CharField(
        "Kiállító", max_length=200, help_text="Pl. Google Skillshop, vagy Udemy · oktató neve."
    )
    category = models.CharField("Kategória", max_length=12, choices=Category.choices, db_index=True)
    kind = models.CharField(
        "Típus",
        max_length=8,
        choices=Kind.choices,
        default=Kind.EXAM,
        help_text="Vizsgával szerzett tanúsítvány, vagy elvégzett kurzus igazolása.",
    )
    issued_on = models.DateField("Kiállítás dátuma")
    expires_on = models.DateField("Lejárat", blank=True, null=True, help_text="Üresen hagyva: nem jár le.")
    hours = models.DecimalField(
        "Óraszám", max_digits=5, decimal_places=1, blank=True, null=True,
        help_text="Kurzusnál a hossza órában (pl. 7.5).",
    )
    credential_url = models.URLField(
        "Ellenőrző link", max_length=500, blank=True,
        help_text="A kiállító oldala, ahol a tanúsítvány ellenőrizhető.",
    )
    credential_id = models.CharField("Tanúsítvány-azonosító", max_length=120, blank=True)
    skills = models.CharField(
        "Képességek", max_length=255, blank=True, help_text="Vesszővel elválasztva: pl. Python, Django, REST API"
    )
    badge_image_url = models.URLField(
        "Jelvény képe", max_length=500, blank=True, help_text="Opcionális kép URL (pl. Cloudinary)."
    )
    order = models.PositiveIntegerField("Sorrend", default=0, help_text="Kategórián belül, kisebb van elöl.")
    is_active = models.BooleanField("Megjelenik", default=True)

    class Meta:
        ordering = ["category", "order", "-issued_on"]
        verbose_name = "Tanúsítvány"
        verbose_name_plural = "Tanúsítványok"

    def __str__(self):
        return f"{self.title} ({self.issuer})"

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    @property
    def is_expired(self):
        return self.expires_on is not None and self.expires_on < timezone.localdate()
