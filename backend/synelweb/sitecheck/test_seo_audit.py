from unittest import mock

from django.test import SimpleTestCase

from . import safe_fetch
from .safe_fetch import FetchError, safe_get
from .seo_audit import _robots_blocks_all, audit_html, run_seo_audit
from .tech_details import tech_details

GOOD_PAGE = b"""<!doctype html><html lang="hu"><head>
<title>Weboldal keszites Sopronban | Pelda Kft.</title>
<meta name="description" content="Egyedi, gyors weboldalak kisvallalkozasoknak Sopronban es kornyeken, szemelyes egyeztetessel es atlathato arakkal.">
<meta name="viewport" content="width=device-width">
<meta property="og:title" content="Pelda"><meta property="og:image" content="https://pelda.hu/og.png">
<link rel="canonical" href="https://pelda.hu/">
<link rel="alternate" hreflang="hu" href="https://pelda.hu/"><link rel="alternate" hreflang="de" href="https://pelda.hu/de">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"LocalBusiness","name":"Pelda"},{"@type":"WebSite"}]}</script>
</head><body><h1>Weboldal keszites</h1><img src="a.png" alt="Logo"><img src="b.png">
<p>""" + b"Szoveg " * 80 + b"""</p></body></html>"""

BARE_PAGE = b"""<html><head><meta name="robots" content="noindex,follow">
<script type="application/ld+json">{ broken json</script></head>
<body><div id="root"></div><script src="/app.js"></script></body></html>"""


def statuses(checks):
    return {check["id"]: check["status"] for check in checks}


class AuditHtmlTests(SimpleTestCase):
    def test_a_well_marked_up_page_passes(self):
        checks, client_rendered = audit_html("https://pelda.hu/", {}, GOOD_PAGE)
        result = statuses(checks)

        for check_id in ("structuredData", "title", "description", "h1", "indexable", "canonical", "viewport", "lang", "social", "hreflang", "https"):
            with self.subTest(check=check_id):
                self.assertEqual(result[check_id], "pass")
        data = {check["id"]: check["data"] for check in checks}
        self.assertEqual(data["structuredData"]["types"], ["LocalBusiness", "WebSite"])
        self.assertEqual(data["images"], {"total": 2, "missingAlt": 1})
        self.assertEqual(result["images"], "warn")
        self.assertFalse(client_rendered)

    def test_a_bare_page_shows_what_is_missing(self):
        checks, client_rendered = audit_html("http://pelda.hu/", {}, BARE_PAGE)
        result = statuses(checks)

        self.assertEqual(result["structuredData"], "fail")  # only a broken block
        self.assertEqual(result["title"], "fail")
        self.assertEqual(result["h1"], "fail")
        self.assertEqual(result["indexable"], "fail")
        self.assertEqual(result["viewport"], "fail")
        self.assertEqual(result["https"], "fail")
        self.assertEqual(result["hreflang"], "info")
        self.assertTrue(client_rendered)

    def test_noindex_in_the_response_header_counts_too(self):
        checks, _ = audit_html("https://pelda.hu/", {"X-Robots-Tag": "noindex"}, GOOD_PAGE)
        self.assertEqual(statuses(checks)["indexable"], "fail")

    def test_types_without_a_business_are_a_hint(self):
        page = GOOD_PAGE.replace(b'"LocalBusiness"', b'"BreadcrumbList"')
        checks, _ = audit_html("https://pelda.hu/", {}, page)
        self.assertEqual(statuses(checks)["structuredData"], "warn")

    def test_robots_txt_blocking_everything(self):
        self.assertTrue(_robots_blocks_all("User-agent: *\nDisallow: /\n"))
        self.assertFalse(_robots_blocks_all("User-agent: *\nDisallow: /admin/\n"))
        self.assertFalse(_robots_blocks_all("User-agent: BadBot\nDisallow: /\n"))


class SafeFetchTests(SimpleTestCase):
    def test_private_and_local_addresses_are_refused(self):
        for address in ("127.0.0.1", "10.0.0.5", "192.168.1.1", "169.254.169.254", "::1", "fc00::1"):
            with self.subTest(address=address), mock.patch.object(
                safe_fetch.socket, "getaddrinfo", return_value=[(None, None, None, "", (address, 443))]
            ):
                with self.assertRaises(FetchError):
                    safe_get("https://csapda.pelda.hu/")

    def test_odd_ports_and_schemes_are_refused(self):
        for url in ("https://pelda.hu:8443/", "ftp://pelda.hu/", "https://user:pw@pelda.hu/"):
            with self.subTest(url=url), self.assertRaises(FetchError):
                safe_get(url)

    @mock.patch.object(safe_fetch.socket, "getaddrinfo")
    @mock.patch.object(safe_fetch.requests, "get")
    def test_a_redirect_to_a_private_address_is_refused(self, get, getaddrinfo):
        getaddrinfo.side_effect = lambda host, *_a, **_k: [
            (None, None, None, "", ("93.184.216.34" if host == "pelda.hu" else "10.0.0.1", 443))
        ]
        get.return_value = mock.Mock(is_redirect=True, headers={"Location": "https://belso.pelda.hu/"})

        with self.assertRaises(FetchError):
            safe_get("https://pelda.hu/")
        get.assert_called_once()

    @mock.patch.object(safe_fetch.socket, "getaddrinfo", return_value=[(None, None, None, "", ("93.184.216.34", 443))])
    @mock.patch.object(safe_fetch.requests, "get")
    def test_the_body_is_cut_at_the_size_limit(self, get, _getaddrinfo):
        get.return_value = mock.Mock(
            is_redirect=False, status_code=200, headers={}, iter_content=lambda chunk_size: iter([b"x" * 600, b"y" * 600])
        )

        _, status, _, body = safe_get("https://pelda.hu/", max_bytes=1000)

        self.assertEqual((status, len(body)), (200, 1000))


class RunSeoAuditTests(SimpleTestCase):
    @mock.patch("sitecheck.seo_audit.safe_get", side_effect=FetchError("unreachable"))
    def test_an_unreachable_page_gives_no_audit(self, _get):
        self.assertIsNone(run_seo_audit("https://pelda.hu/"))

    @mock.patch("sitecheck.seo_audit.safe_get")
    def test_adds_robots_and_sitemap_checks(self, get):
        def fake(url, **_kwargs):
            if url.endswith("/robots.txt"):
                return url, 200, {}, b"User-agent: *\nAllow: /\nSitemap: https://pelda.hu/sitemap.xml\n"
            if url.endswith("/sitemap.xml"):
                return url, 200, {}, b"<?xml version='1.0'?><urlset></urlset>"
            return url, 200, {}, GOOD_PAGE

        get.side_effect = fake
        audit = run_seo_audit("https://pelda.hu/")

        result = statuses(audit["checks"])
        self.assertEqual((result["robots"], result["sitemap"]), ("pass", "pass"))


class TechDetailsTests(SimpleTestCase):
    def test_counts_fonts_scripts_and_cache_from_the_report(self):
        requests = (
            [{"resourceType": "Font", "transferSize": 30 * 1024}] * 6
            + [{"resourceType": "Script", "transferSize": 400 * 1024}, {"resourceType": "Script", "transferSize": 20 * 1024}]
            + [{"resourceType": "Document", "transferSize": 50 * 1024}]
        )
        audits = {
            "network-requests": {"details": {"items": requests}},
            "uses-long-cache-ttl": {"details": {"items": [{}, {}, {}]}},
            "unused-javascript": {"details": {"overallSavingsBytes": 200 * 1024}},
            "dom-size": {"numericValue": 900},
        }

        details = {item["id"]: item for item in tech_details(audits)}

        self.assertEqual(details["fonts"]["data"], {"count": 6, "kb": 180})
        self.assertEqual(details["fonts"]["status"], "warn")
        self.assertEqual(details["javascript"]["data"], {"count": 2, "kb": 420, "unusedKb": 200})
        self.assertEqual(details["javascript"]["status"], "warn")
        self.assertEqual(details["codeSplitting"], {"id": "codeSplitting", "status": "warn", "data": {"largestKb": 400}})
        self.assertEqual(details["cache"]["data"], {"shortCache": 3})
        self.assertEqual(details["domSize"]["status"], "pass")

    def test_no_network_data_gives_no_details(self):
        self.assertEqual(tech_details({}), [])
