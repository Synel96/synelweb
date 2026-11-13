from unittest import mock

from django.contrib.admin.sites import AdminSite
from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .admin import QuoteRequestAdmin
from .models import QuoteRequest
from .notifications import notify_new_quote

URL = "/api/quote-requests/"

SIMPLE = {
    "mode": "simple",
    "service": "landing-oldal",
    "serviceName": "Landing oldal",
    "name": "Teszt Elek",
    "email": "teszt@pelda.hu",
    "message": "Egy egyoldalas bemutatkozó oldalt szeretnék.",
    "consent": True,
    "siteLanguage": "hu",
}

DETAILED = {
    **SIMPLE,
    "mode": "detailed",
    "phone": "+36 30 123 4567",
    "existingSite": "renew",
    "websiteUrl": "https://pelda.hu",
    "domain": "has",
    "domainName": "pelda.hu",
    "size": "few_pages",
    "languages": ["hu", "de"],
    "addons": ["google_search_ads", "business_email"],
    "timeline": "one_two_months",
    "budget": "200k_400k",
    "isLocal": True,
    "isGrantFunded": False,
    "contactPreference": "online",
}


ADS = {
    **SIMPLE,
    "mode": "detailed",
    "service": "google-ads",
    "serviceName": "Csak hirdetési kampány (Google Ads)",
    "message": "Keresőhirdetést szeretnék a meglévő oldalamhoz.",
    "websiteUrl": "https://pelda.hu",
    "languages": ["hu"],
    "adsAccount": "none",
    "adBudget": "60k_150k",
    "timeline": "urgent",
}


class QuoteRequestAPITests(APITestCase):
    def post(self, payload):
        # secure: production settings redirect plain HTTP to HTTPS.
        return self.client.post(URL, payload, format="json", secure=True)

    def setUp(self):
        cache.clear()

    def test_url_is_the_api_alias(self):
        self.assertEqual(reverse("quote-request-create"), URL)

    def test_simple_request_is_saved(self):
        response = self.post(SIMPLE)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quote = QuoteRequest.objects.get()
        self.assertEqual(quote.mode, "simple")
        self.assertEqual(quote.service, "landing-oldal")
        self.assertEqual(quote.service_name, "Landing oldal")
        self.assertEqual(quote.status, "new")
        self.assertTrue(quote.consent)

    def test_detailed_request_keeps_its_details(self):
        response = self.post(DETAILED)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quote = QuoteRequest.objects.get()
        self.assertEqual(quote.existing_site, "renew")
        self.assertEqual(quote.domain, "has")
        self.assertEqual(quote.domain_name, "pelda.hu")
        self.assertEqual(quote.languages, ["hu", "de"])
        self.assertEqual(quote.addons, ["google_search_ads", "business_email"])
        self.assertEqual(quote.budget, "200k_400k")
        self.assertTrue(quote.is_local)
        self.assertEqual(quote.contact_preference, "online")

    def test_ads_request_keeps_the_ads_details(self):
        response = self.post(ADS)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quote = QuoteRequest.objects.get()
        self.assertTrue(quote.is_ads_request())
        self.assertEqual(quote.ads_account, "none")
        self.assertEqual(quote.ad_budget, "60k_150k")
        self.assertEqual(quote.website_url, "https://pelda.hu")

    def test_unknown_ad_budget_is_rejected(self):
        response = self.post({**ADS, "adBudget": "1m"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_simple_request_drops_detail_fields(self):
        response = self.post({**DETAILED, "mode": "simple"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quote = QuoteRequest.objects.get()
        self.assertEqual(quote.addons, [])
        self.assertEqual(quote.budget, "")
        self.assertFalse(quote.is_local)

    def test_domain_name_is_kept_only_when_there_is_a_domain(self):
        response = self.post({**DETAILED, "domain": "none", "domainName": "pelda.hu"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        quote = QuoteRequest.objects.get()
        self.assertEqual(quote.domain, "none")
        self.assertEqual(quote.domain_name, "")

    def test_consent_is_required(self):
        for consent in (False, None):
            payload = {**SIMPLE, "consent": consent}
            response = self.post(payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        payload = {key: value for key, value in SIMPLE.items() if key != "consent"}
        self.assertEqual(
            self.post(payload).status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(QuoteRequest.objects.exists())

    def test_only_the_offered_addons_are_accepted(self):
        response = self.post({**DETAILED, "addons": ["hosting_and_domain"]})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("addons", response.data)

    def test_missing_contact_details_are_rejected(self):
        response = self.post({**SIMPLE, "email": "nem-email"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_honeypot_is_accepted_but_not_saved(self):
        with mock.patch("quotes.views.notify_new_quote") as notify:
            response = self.post({**SIMPLE, "company": "Spam Kft."})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(QuoteRequest.objects.exists())
        notify.assert_not_called()

    def test_new_request_triggers_notification(self):
        with mock.patch("quotes.views.notify_new_quote") as notify:
            self.post(SIMPLE)

        notify.assert_called_once_with(QuoteRequest.objects.get())

    def test_too_many_requests_are_throttled(self):
        with mock.patch(
            "rest_framework.throttling.ScopedRateThrottle.THROTTLE_RATES",
            {"quote_requests": "2/hour"},
        ):
            codes = [self.post(SIMPLE).status_code for _ in range(3)]

        self.assertEqual(codes[:2], [201, 201])
        self.assertEqual(codes[2], status.HTTP_429_TOO_MANY_REQUESTS)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class QuoteNotificationTests(TestCase):
    def _quote(self, **overrides):
        data = {
            "mode": "detailed",
            "service": "7",
            "service_name": "Webshop",
            "name": "Teszt Elek",
            "email": "teszt@pelda.hu",
            "message": "Webshopot szeretnék.",
            "addons": ["google_search_ads"],
            "languages": ["hu", "en"],
            "domain": "has",
            "domain_name": "pelda.hu",
            "consent": True,
        }
        data.update(overrides)
        return QuoteRequest.objects.create(**data)

    @override_settings(QUOTE_NOTIFY_EMAIL="", EMAIL_HOST="smtp.pelda.hu")
    def test_no_mail_without_a_recipient(self):
        self.assertFalse(notify_new_quote(self._quote(), run_async=False))
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(QUOTE_NOTIFY_EMAIL="info@synelweb.hu", EMAIL_HOST="")
    def test_no_mail_without_a_mail_server(self):
        self.assertFalse(notify_new_quote(self._quote(), run_async=False))
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(QUOTE_NOTIFY_EMAIL="info@synelweb.hu", EMAIL_HOST="smtp.pelda.hu")
    def test_mail_lists_the_request(self):
        self.assertTrue(notify_new_quote(self._quote(), run_async=False))

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.to, ["info@synelweb.hu"])
        self.assertEqual(message.reply_to, ["teszt@pelda.hu"])
        self.assertIn("Google keresőhirdetés", message.body)
        self.assertIn("Magyar, Angol", message.body)
        self.assertIn("Domain: Van domainje (pelda.hu)", message.body)
        self.assertIn("Szolgáltatás: Webshop (7)", message.body)
        self.assertEqual(message.subject, "Új ajánlatkérés: Teszt Elek (Webshop)")

    @override_settings(QUOTE_NOTIFY_EMAIL="info@synelweb.hu", EMAIL_HOST="smtp.pelda.hu")
    def test_mail_lists_the_ads_details_for_an_ads_request(self):
        quote = self._quote(
            service="google-ads",
            service_name="Csak hirdetési kampány (Google Ads)",
            ads_account="has",
            ad_budget="150k_300k",
            website_url="https://pelda.hu",
            addons=[],
        )
        notify_new_quote(quote, run_async=False)

        body = mail.outbox[0].body
        self.assertIn("Részletek (hirdetési kampány):", body)
        self.assertIn("Google Ads fiók: Van Google Ads fiókja", body)
        self.assertIn("Havi hirdetési keret: 150 000 – 300 000 Ft", body)
        self.assertIn("Weboldal: https://pelda.hu", body)
        self.assertNotIn("Domain:", body)

    @override_settings(QUOTE_NOTIFY_EMAIL="info@synelweb.hu", EMAIL_HOST="smtp.pelda.hu")
    def test_mail_failure_does_not_raise(self):
        with mock.patch("quotes.notifications.EmailMessage.send", side_effect=OSError):
            notify_new_quote(self._quote(), run_async=False)


class QuoteRequestModelTests(TestCase):
    def test_service_display_without_a_name_falls_back_to_the_id(self):
        quote = QuoteRequest(service="unsure")
        self.assertEqual(quote.service_display(), "unsure")


class QuoteRequestAdminTests(TestCase):
    def test_admin_shows_labels_and_cannot_add(self):
        quote = QuoteRequest.objects.create(
            mode="detailed",
            service="webshop",
            name="Teszt",
            email="t@pelda.hu",
            message="Webshop kellene.",
            addons=["business_email", "cookieless_analytics"],
            consent=True,
        )
        admin = QuoteRequestAdmin(QuoteRequest, AdminSite())

        self.assertEqual(
            admin.addons_display(quote), "Céges e-mail, Süti-mentes weboldal-analitika"
        )
        self.assertFalse(admin.has_add_permission(request=None))
