from unittest import mock

from django.contrib.admin.sites import AdminSite
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Review

from .admin import ReviewAdmin

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


@override_settings(VERCEL_DEPLOY_HOOK_URL="https://api.vercel.com/v1/integrations/deploy/test")
class ApproveReviewsActionTest(TestCase):
    def setUp(self):
        self.admin = ReviewAdmin(Review, AdminSite())
        self.approved = Review.objects.create(name="Mar jovahagyott", rating=5, is_approved=True)
        self.pending = Review.objects.create(name="Fuggoben", rating=4, is_approved=False)

    @mock.patch("review.admin.trigger_vercel_deploy")
    def test_bulk_approve_triggers_deploy_once_when_new_reviews_are_approved(self, mock_trigger):
        queryset = Review.objects.filter(pk__in=[self.approved.pk, self.pending.pk])
        self.admin.approve_reviews(request=None, queryset=queryset)

        self.pending.refresh_from_db()
        self.assertTrue(self.pending.is_approved)
        mock_trigger.assert_called_once_with("reviews approved")

    @mock.patch("review.admin.trigger_vercel_deploy")
    def test_bulk_approve_is_a_noop_when_nothing_new_is_approved(self, mock_trigger):
        queryset = Review.objects.filter(pk=self.approved.pk)
        self.admin.approve_reviews(request=None, queryset=queryset)

        mock_trigger.assert_not_called()