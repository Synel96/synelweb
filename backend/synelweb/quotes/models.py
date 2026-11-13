from django.db import models


class QuoteRequest(models.Model):
    """A quote request sent from the site's contact page.

    The form has a simplified and a detailed mode; the detailed-only fields
    are optional and stay empty for simplified requests.
    """

    class Mode(models.TextChoices):
        SIMPLE = "simple", "Egyszerűsített"
        DETAILED = "detailed", "Részletes"

    class Status(models.TextChoices):
        NEW = "new", "Új"
        CONTACTED = "contacted", "Felvettem a kapcsolatot"
        CLOSED = "closed", "Lezárva"

    class ExistingSite(models.TextChoices):
        NONE = "none", "Nincs még weboldala"
        RENEW = "renew", "Van, megújítaná"
        EXTEND = "extend", "Van, bővítené"

    class Domain(models.TextChoices):
        HAS = "has", "Van domainje"
        NONE = "none", "Nincs még domainje"
        UNSURE = "unsure", "Nem tudja"

    class Size(models.TextChoices):
        ONE_PAGE = "one_page", "1 oldal"
        FEW_PAGES = "few_pages", "3–5 oldal"
        MANY_PAGES = "many_pages", "5+ oldal"
        UNSURE = "unsure", "Még nem tudja"

    class Timeline(models.TextChoices):
        URGENT = "urgent", "Sürgős"
        ONE_TWO_MONTHS = "one_two_months", "1–2 hónap"
        FLEXIBLE = "flexible", "Rugalmas"

    class Budget(models.TextChoices):
        UNDER_200K = "under_200k", "200 000 Ft alatt"
        FROM_200K_TO_400K = "200k_400k", "200 000 – 400 000 Ft"
        FROM_400K_TO_800K = "400k_800k", "400 000 – 800 000 Ft"
        OVER_800K = "over_800k", "800 000 Ft felett"
        UNSURE = "unsure", "Még nem tudja"

    class AdsAccount(models.TextChoices):
        HAS = "has", "Van Google Ads fiókja"
        NONE = "none", "Nincs még fiókja"
        UNSURE = "unsure", "Nem tudja"

    class AdBudget(models.TextChoices):
        UNDER_60K = "under_60k", "60 000 Ft alatt"
        FROM_60K_TO_150K = "60k_150k", "60 000 – 150 000 Ft"
        FROM_150K_TO_300K = "150k_300k", "150 000 – 300 000 Ft"
        OVER_300K = "over_300k", "300 000 Ft felett"
        UNSURE = "unsure", "Még nem tudja"

    # The service id of "only an ad campaign" (priced in the frontend, not a
    # Package): its detailed requests carry the ads fields instead of the
    # website ones.
    ADS_SERVICE = "google-ads"

    class ContactPreference(models.TextChoices):
        EMAIL = "email", "E-mail"
        PHONE = "phone", "Telefon"
        ONLINE = "online", "Online megbeszélés"
        IN_PERSON = "in_person", "Személyesen"

    ADDONS = {
        "business_email": "Céges e-mail",
        "google_search_ads": "Google keresőhirdetés",
        "cookieless_analytics": "Süti-mentes weboldal-analitika",
    }
    LANGUAGES = {"hu": "Magyar", "en": "Angol", "de": "Német"}

    mode = models.CharField("Űrlap", max_length=10, choices=Mode.choices)
    status = models.CharField(
        "Állapot", max_length=10, choices=Status.choices, default=Status.NEW, db_index=True
    )

    service = models.CharField(
        "Szolgáltatás",
        max_length=120,
        help_text="A választott szolgáltatás azonosítója, vagy 'unsure'.",
    )
    service_name = models.CharField(
        "Szolgáltatás neve",
        max_length=200,
        blank=True,
        help_text="Ahogy a látogató az űrlapon látta.",
    )
    name = models.CharField("Név", max_length=120)
    email = models.EmailField("E-mail")
    phone = models.CharField("Telefon", max_length=40, blank=True)
    message = models.TextField("Üzenet", max_length=4000)

    existing_site = models.CharField(
        "Meglévő weboldal", max_length=10, choices=ExistingSite.choices, blank=True
    )
    website_url = models.CharField("Weboldal címe", max_length=300, blank=True)
    domain = models.CharField("Domain", max_length=10, choices=Domain.choices, blank=True)
    domain_name = models.CharField("Domain neve", max_length=253, blank=True)
    size = models.CharField("Méret", max_length=12, choices=Size.choices, blank=True)
    languages = models.JSONField("Nyelvek", default=list, blank=True)
    addons = models.JSONField("Kiegészítők", default=list, blank=True)
    timeline = models.CharField(
        "Határidő", max_length=16, choices=Timeline.choices, blank=True
    )
    budget = models.CharField("Keretösszeg", max_length=12, choices=Budget.choices, blank=True)
    ads_account = models.CharField(
        "Google Ads fiók", max_length=10, choices=AdsAccount.choices, blank=True
    )
    ad_budget = models.CharField(
        "Havi hirdetési keret", max_length=12, choices=AdBudget.choices, blank=True
    )
    is_local = models.BooleanField("Sopron környéki", default=False)
    is_grant_funded = models.BooleanField("Pályázati forrásból", default=False)
    contact_preference = models.CharField(
        "Egyeztetés módja", max_length=10, choices=ContactPreference.choices, blank=True
    )

    site_language = models.CharField("Oldal nyelve", max_length=2, default="hu")
    consent = models.BooleanField("Adatkezelési hozzájárulás", default=False)
    created_at = models.DateTimeField("Beérkezett", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ajánlatkérés"
        verbose_name_plural = "Ajánlatkérések"

    def __str__(self):
        return f"{self.name} – {self.service_display()} ({self.get_mode_display()})"

    def service_display(self):
        """The name the visitor picked, with the id for reference."""
        if self.service_name and self.service_name != self.service:
            return f"{self.service_name} ({self.service})"
        return self.service

    def is_ads_request(self):
        return self.service == self.ADS_SERVICE

    def addon_labels(self):
        return [self.ADDONS.get(key, key) for key in self.addons]

    def language_labels(self):
        return [self.LANGUAGES.get(key, key) for key in self.languages]
