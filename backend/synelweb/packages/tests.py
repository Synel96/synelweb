from unittest import mock
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Package

class PackageListAPITest(APITestCase):
    def setUp(self):
        Package.objects.create(
            name="Teszt Csomag",
            slug="teszt-csomag",
            preview_image_url="https://pelda.hu/csomag.png",
            description="Ez egy teszt csomag.",
            is_discounted=True,
            tags="seo, statikus oldal",
        )

    def test_package_list_api_returns_packages(self):
        url = reverse("package-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Teszt Csomag")

class ExchangeRateAPITest(APITestCase):
    URL = "/api/exchange-rates/"

    def get(self):
        # secure: production settings redirect plain HTTP to HTTPS.
        return self.client.get(self.URL, secure=True)

    def test_returns_the_cached_rates(self):
        from .models import ExchangeRate

        ExchangeRate.objects.create(target_currency="EUR", rate="0.002500")
        ExchangeRate.objects.create(target_currency="USD", rate="0.002750")

        with mock.patch("packages.currency.fetch_rates") as fetch:
            response = self.get()

        fetch.assert_not_called()  # fresh enough, no refresh
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["base"], "HUF")
        self.assertEqual(response.data["rates"], {"USD": 0.00275, "EUR": 0.0025})
        self.assertIn("max-age=3600", response["Cache-Control"])

    def test_leaves_out_a_currency_without_a_rate(self):
        import requests

        with mock.patch("packages.currency.fetch_rates", side_effect=requests.RequestException):
            response = self.get()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["rates"], {})


class PackageApiCategoryAndMonthlyPriceTest(APITestCase):
    URL = "/api/services/"

    def get(self, lang="hu"):
        return self.client.get(self.URL, secure=True, HTTP_ACCEPT_LANGUAGE=lang)

    def test_exposes_category_and_monthly_price(self):
        Package.objects.create(
            name="Google keresőhirdetés",
            slug="google-keresohirdetes",
            description="Hirdetéskezelés",
            category=Package.Category.MARKETING,
            price=60000,
            monthly_price=30000,
        )
        Package.objects.create(name="Landing oldal", slug="landing", description="Egy oldal", price=149000)

        data = {item["title"]["hu"]: item for item in self.get().data}

        ads = data["Google keresőhirdetés"]
        self.assertEqual(ads["category"], "marketing")
        self.assertEqual(ads["price"], {"amount": 60000.0, "currency": "HUF"})
        self.assertEqual(ads["monthlyPrice"], {"amount": 30000.0, "currency": "HUF"})
        landing = data["Landing oldal"]
        self.assertEqual(landing["category"], "website")
        self.assertIsNone(landing["monthlyPrice"])

    def test_blank_localized_slug_falls_back_to_the_stored_slug(self):
        import json

        Package.objects.create(
            name="Webshop",
            slug="webshop",
            description=json.dumps(
                {"title": {"hu": "Webshop"}, "slug": {"hu": "", "en": "", "de": "online-shop"}}
            ),
        )

        slug = self.get().data[0]["slug"]

        self.assertEqual(slug, {"hu": "webshop", "en": "webshop", "de": "online-shop"})
