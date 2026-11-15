from django.db import models


class SiteCheck(models.Model):
    """One website measurement run from the site's free checker.

    Kept so the admin shows which sites visitors check (a lead signal). No
    personal data: only the checked URL and the scores.
    """

    class Strategy(models.TextChoices):
        MOBILE = "mobile", "Mobil"
        DESKTOP = "desktop", "Asztali"

    url = models.URLField("Ellenőrzött oldal", max_length=500)
    strategy = models.CharField("Eszköz", max_length=10, choices=Strategy.choices)
    site_language = models.CharField("Oldal nyelve", max_length=2, default="hu")
    performance = models.PositiveSmallIntegerField("Teljesítmény", null=True, blank=True)
    accessibility = models.PositiveSmallIntegerField("Akadálymentesség", null=True, blank=True)
    best_practices = models.PositiveSmallIntegerField("Bevált gyakorlatok", null=True, blank=True)
    seo = models.PositiveSmallIntegerField("SEO", null=True, blank=True)
    created_at = models.DateTimeField("Mérve", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Weboldal-ellenőrzés"
        verbose_name_plural = "Weboldal-ellenőrzések"

    def __str__(self):
        return f"{self.url} ({self.get_strategy_display()})"
