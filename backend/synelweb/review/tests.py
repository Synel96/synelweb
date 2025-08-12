from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Review

class ReviewListAPITest(APITestCase):
    def setUp(self):
        Review.objects.create(
            name="Teszt Elek",
            email="teszt@pelda.hu",
            rating=5,
            comment="Nagyon jó!",
        )
        Review.objects.create(
            name="Második Teszt",
            email="masodik@pelda.hu",
            rating=4,
            comment="Elégedett vagyok.",
        )

    def test_review_list_api_returns_reviews(self):
        url = reverse("review-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Sorrend helyett csak azt ellenőrizzük, hogy mindkét név szerepel a válaszban
        names = [item["name"] for item in response.data]
        self.assertIn("Teszt Elek", names)
        self.assertIn("Második Teszt", names)