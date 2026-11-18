from unittest import mock

from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .models import SiteCheck
from .pagespeed import PageSpeedError, _summarise

URL = "/api/site-check/"

PSI_RESPONSE = {
    "lighthouseResult": {
        "finalDisplayedUrl": "https://pelda.hu/",
        "categories": {
            "performance": {"score": 0.62},
            "accessibility": {"score": 0.91},
            "best-practices": {"score": 1},
            "seo": {"score": 0.83},
        },
        "audits": {
            "largest-contentful-paint": {
                "id": "largest-contentful-paint",
                "title": "Largest Contentful Paint",
                "displayValue": "4,1 s",
                "score": 0.2,
            },
            "cumulative-layout-shift": {
                "id": "cumulative-layout-shift",
                "title": "Cumulative Layout Shift",
                "displayValue": "0,02",
                "score": 1,
            },
            "uses-optimized-images": {
                "id": "uses-optimized-images",
                "title": "Képek hatékony kódolása",
                "displayValue": "Lehetséges megtakarítás: 320 KiB",
                "score": 0.3,
                "details": {"type": "opportunity", "overallSavingsMs": 1200},
            },
            "render-blocking-resources": {
                "id": "render-blocking-resources",
                "title": "Távolítsa el a megjelenítést gátló erőforrásokat",
                "score": 0.4,
                "details": {"type": "opportunity", "overallSavingsMs": 2100},
            },
            "already-good": {
                "id": "already-good",
                "title": "Rendben",
                "score": 1,
                "details": {"type": "opportunity", "overallSavingsMs": 50},
            },
        },
    },
    "loadingExperience": {
        "metrics": {
            "LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 3200, "category": "AVERAGE"},
            "CUMULATIVE_LAYOUT_SHIFT_SCORE": {"percentile": 5, "category": "FAST"},
        }
    },
}

SUMMARY = _summarise(PSI_RESPONSE)


# Newer Lighthouse: insights with metricSavings instead of opportunities.
INSIGHTS_RESPONSE = {
    "lighthouseResult": {
        "categories": {
            "performance": {
                "score": 0.72,
                "auditRefs": [
                    {"id": "largest-contentful-paint", "group": "metrics"},
                    {"id": "cls-culprits-insight", "group": "insights"},
                    {"id": "render-blocking-insight", "group": "insights"},
                    {"id": "image-delivery-insight", "group": "insights"},
                    {"id": "dom-size-insight", "group": "insights"},
                ],
            },
        },
        "audits": {
            "largest-contentful-paint": {"id": "largest-contentful-paint", "title": "LCP", "score": 0.4},
            "cls-culprits-insight": {
                "id": "cls-culprits-insight",
                "title": "Layout shift culprits",
                "score": 0,
                "scoreDisplayMode": "metricSavings",
                "metricSavings": {"CLS": 0.384},
            },
            "render-blocking-insight": {
                "id": "render-blocking-insight",
                "title": "Render blocking requests",
                "score": 0.5,
                "scoreDisplayMode": "metricSavings",
                "metricSavings": {"FCP": 600, "LCP": 600},
            },
            "image-delivery-insight": {
                "id": "image-delivery-insight",
                "title": "Improve image delivery",
                "score": 1,
                "scoreDisplayMode": "metricSavings",
                "metricSavings": {"LCP": 0},
            },
            "dom-size-insight": {
                "id": "dom-size-insight",
                "title": "Optimize DOM size",
                "score": None,
                "scoreDisplayMode": "informative",
            },
        },
    },
}


class SummaryTests(TestCase):
    def test_reads_newer_insights_including_layout_shift(self):
        summary = _summarise(INSIGHTS_RESPONSE)

        self.assertEqual(
            [(o["id"], o["savingsMs"], o["clsSavings"]) for o in summary["opportunities"]],
            [("cls-culprits-insight", 0, 0.384), ("render-blocking-insight", 600, 0)],
        )

    def test_keeps_scores_metrics_and_biggest_wins_first(self):
        self.assertEqual(
            SUMMARY["scores"],
            {"performance": 62, "accessibility": 91, "bestPractices": 100, "seo": 83},
        )
        self.assertEqual(SUMMARY["finalUrl"], "https://pelda.hu/")
        self.assertEqual([m["id"] for m in SUMMARY["lab"]], ["largest-contentful-paint", "cumulative-layout-shift"])
        self.assertEqual([m["id"] for m in SUMMARY["field"]], ["lcp", "cls"])
        self.assertEqual(
            [o["id"] for o in SUMMARY["opportunities"]],
            ["render-blocking-resources", "uses-optimized-images"],
        )


SEO_AUDIT = {"finalUrl": "https://pelda.hu/", "checks": [{"id": "h1", "status": "pass", "data": {"count": 1}}], "clientRendered": False}


class SiteCheckAPITests(APITestCase):
    def setUp(self):
        cache.clear()
        # The SEO audit fetches the page itself; never over the network here.
        patcher = mock.patch("sitecheck.views.run_seo_audit", return_value=SEO_AUDIT)
        self.seo_audit = patcher.start()
        self.addCleanup(patcher.stop)

    def post(self, payload, ip="203.0.113.10"):
        # The client address as Fly's proxy appends it (NUM_PROXIES = 1).
        return self.client.post(
            URL, payload, format="json", secure=True, HTTP_X_FORWARDED_FOR=ip, REMOTE_ADDR="10.0.0.1"
        )

    @mock.patch("sitecheck.views.run_pagespeed", return_value=SUMMARY)
    def test_checks_a_site_adding_https_and_records_it(self, run):
        response = self.post({"url": "pelda.hu", "strategy": "mobile", "lang": "hu"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        run.assert_called_once_with("https://pelda.hu", "mobile", "hu")
        self.assertEqual(response.data["scores"]["performance"], 62)
        self.assertEqual(response.data["seo"], SEO_AUDIT)
        self.seo_audit.assert_called_once_with("https://pelda.hu")
        check = SiteCheck.objects.get()
        self.assertEqual((check.url, check.strategy, check.performance), ("https://pelda.hu", "mobile", 62))

    @mock.patch("sitecheck.views.run_pagespeed", return_value=SUMMARY)
    def test_repeated_checks_are_served_from_the_cache(self, run):
        self.post({"url": "https://pelda.hu", "strategy": "desktop"})
        self.post({"url": "https://pelda.hu", "strategy": "desktop"})

        run.assert_called_once()
        self.assertEqual(SiteCheck.objects.count(), 1)

    def test_rejects_what_is_not_a_public_website(self):
        for url in ["nem egy oldal", "localhost", "http://127.0.0.1", "ftp://pelda.hu"]:
            with self.subTest(url=url):
                self.assertEqual(self.post({"url": url}).status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch("sitecheck.views.run_pagespeed", return_value=SUMMARY)
    def test_a_failing_seo_audit_does_not_break_the_check(self, _run):
        self.seo_audit.side_effect = RuntimeError("boom")

        response = self.post({"url": "https://pelda.hu"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["seo"])

    @mock.patch("sitecheck.views.run_pagespeed", return_value=SUMMARY)
    def test_too_many_checks_in_a_row_are_refused(self, _run):
        from .throttles import SiteCheckBurstThrottle

        with mock.patch.object(SiteCheckBurstThrottle, "THROTTLE_RATES", {"site_checks_burst": "2/min"}):
            codes = [self.post({"url": f"https://pelda{n}.hu"}).status_code for n in range(3)]

        self.assertEqual(codes, [200, 200, status.HTTP_429_TOO_MANY_REQUESTS])

    @mock.patch("sitecheck.views.run_pagespeed", return_value=SUMMARY)
    def test_the_daily_ceiling_applies_to_all_visitors_together(self, _run):
        from .throttles import SiteCheckGlobalThrottle

        with mock.patch.object(SiteCheckGlobalThrottle, "THROTTLE_RATES", {"site_checks_global": "1/day"}):
            first = self.post({"url": "https://pelda.hu"}, ip="203.0.113.1")
            second = self.post({"url": "https://masik.hu"}, ip="203.0.113.2")

        self.assertEqual((first.status_code, second.status_code), (200, status.HTTP_429_TOO_MANY_REQUESTS))

    @mock.patch("sitecheck.views.run_pagespeed", return_value=SUMMARY)
    def test_a_check_is_refused_while_too_many_are_running(self, run):
        from . import views

        with mock.patch.object(views, "_running_checks", mock.Mock(acquire=mock.Mock(return_value=False))):
            response = self.post({"url": "https://pelda.hu"})

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data, {"error": "busy"})
        run.assert_not_called()

    @mock.patch("sitecheck.views.run_pagespeed", side_effect=PageSpeedError("unreachable"))
    def test_an_unreachable_site_is_reported(self, _run):
        response = self.post({"url": "https://nincs-ilyen-oldal.hu"})

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data, {"error": "unreachable"})
        self.assertEqual(SiteCheck.objects.count(), 0)


@override_settings(PAGESPEED_API_KEY="kulcs", PAGESPEED_TIMEOUT=5)
class PageSpeedClientTests(TestCase):
    @mock.patch("sitecheck.pagespeed.requests.get")
    def test_sends_the_key_locale_and_all_categories(self, get):
        from .pagespeed import run_pagespeed

        get.return_value = mock.Mock(ok=True, status_code=200, json=lambda: PSI_RESPONSE)
        run_pagespeed("https://pelda.hu", "mobile", "de")

        params = get.call_args.kwargs["params"]
        self.assertIn(("key", "kulcs"), params)
        self.assertIn(("locale", "de"), params)
        self.assertEqual([v for k, v in params if k == "category"], ["performance", "accessibility", "best-practices", "seo"])

    @mock.patch("sitecheck.pagespeed.requests.get")
    def test_maps_google_errors(self, get):
        from .pagespeed import run_pagespeed

        for code, expected in [(400, "unreachable"), (429, "quota"), (500, "upstream")]:
            get.return_value = mock.Mock(ok=False, status_code=code)
            with self.subTest(code=code), self.assertRaises(PageSpeedError) as raised:
                run_pagespeed("https://pelda.hu", "mobile", "hu")
            self.assertEqual(raised.exception.code, expected)
