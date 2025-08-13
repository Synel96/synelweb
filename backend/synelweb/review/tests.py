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
        names = [item["name"] for item in response.data]
        self.assertIn("Teszt Elek", names)
        self.assertIn("Második Teszt", names)

    def test_review_create_api(self):
        url = reverse("review-list")
        data = {
            "name": "Új Teszt",
            "email": "ujteszt@pelda.hu",
            "rating": 5,
            "comment": "Szuper!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 3)
        self.assertTrue(Review.objects.filter(name="Új Teszt").exists())