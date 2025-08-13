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