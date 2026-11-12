import datetime
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Certificate

URL = "/api/certificates/"


class CertificateAPITests(APITestCase):
    def get(self):
        # secure: production settings redirect plain HTTP to HTTPS.
        return self.client.get(URL, secure=True)

    def test_url_is_the_api_alias(self):
        self.assertEqual(reverse("api-certificates"), URL)

    def test_seeded_certificates_are_listed_by_category_and_order(self):
        data = self.get().data

        self.assertEqual(
            [(c["category"], c["title"].split()[0]) for c in data],
            [
                ("backend", "PCEP™"),
                ("backend", "Build"),
                ("fullstack", "Django"),  # same order: newest first
                ("fullstack", "Become"),
                ("marketing", "Google"),
            ],
        )

    def test_fields_are_camel_case_with_skills_as_a_list(self):
        ads = next(c for c in self.get().data if c["category"] == "marketing")

        self.assertEqual(ads["kind"], "exam")
        self.assertEqual(ads["issuedOn"], "2026-11-08")
        self.assertEqual(ads["expiresOn"], "2027-11-08")
        self.assertEqual(ads["skills"], ["Google Ads", "Search Ads", "Keywords"])
        self.assertTrue(ads["credentialUrl"].startswith("https://skillshop.credential.net/"))

        course = next(c for c in self.get().data if c["title"].startswith("Become"))
        self.assertEqual(course["kind"], "course")
        self.assertEqual(course["hours"], 7.5)
        self.assertIsNone(course["expiresOn"])

    def test_hidden_certificates_are_left_out(self):
        Certificate.objects.update(is_active=False)

        self.assertEqual(self.get().data, [])

    def test_expired_flag(self):
        cert = Certificate.objects.get(category="marketing")
        cert.expires_on = datetime.date(2020, 1, 1)
        cert.save()

        ads = next(c for c in self.get().data if c["category"] == "marketing")
        self.assertTrue(ads["isExpired"])


class CertificateDeployHookTests(TestCase):
    def test_saving_and_deleting_rebuild_the_site(self):
        with mock.patch("certificates.signals.trigger_vercel_deploy") as deploy:
            with self.captureOnCommitCallbacks(execute=True):
                cert = Certificate.objects.create(
                    title="Teszt", issuer="Teszt", category="frontend", issued_on=datetime.date(2025, 1, 1)
                )
            with self.captureOnCommitCallbacks(execute=True):
                cert.delete()

        self.assertEqual(
            [call.args[0] for call in deploy.call_args_list],
            ["certificate created", "certificate deleted"],
        )
