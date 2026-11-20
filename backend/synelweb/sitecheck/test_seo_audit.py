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


class PlatformTests(SimpleTestCase):
    def detect(self, html, headers=None):
        from .platform import detect_platform

        return detect_platform(html, headers)

    def test_wordpress_with_its_page_builder_theme_and_shop(self):
        html = (
            '<link href="https://pelda.hu/wp-content/themes/astra/style.css">'
            '<div class="elementor-section"></div><body class="woocommerce">'
        )
        self.assertEqual(
            self.detect(html),
            {
                "builder": "WordPress",
                "addons": ["Elementor", "WooCommerce"],
                "theme": "astra",
                "frameworks": [],
                "generator": "",
                "kind": "builder",
            },
        )

    def test_site_builders(self):
        cases = {
            "Wix": '<img src="https://static.wixstatic.com/media/a.jpg">',
            "Shopify": '<script>Shopify.theme = {"name":"Dawn","id":1}</script><script src="//cdn.shopify.com/s.js"></script>',
            "Webflow": '<html data-wf-page="123" data-wf-site="456">',
            "Squarespace": '<link href="https://static1.squarespace.com/static/x.css">',
        }
        for builder, html in cases.items():
            with self.subTest(builder=builder):
                result = self.detect(html)
                self.assertEqual((result["builder"], result["kind"]), (builder, "builder"))
        self.assertEqual(self.detect(cases["Shopify"])["theme"], "dawn")

    def test_a_custom_build_names_its_framework(self):
        result = self.detect('<script id="__NEXT_DATA__" type="application/json">{}</script><script src="/_next/static/a.js"></script>')
        self.assertEqual((result["builder"], result["frameworks"], result["kind"]), (None, ["Next.js"], "custom"))
        self.assertEqual(self.detect('<script id="vike_pageContext" type="application/json"></script>')["frameworks"], ["Vike"])

    def test_headers_and_nothing_found(self):
        self.assertEqual(self.detect("<html></html>", {"X-Wix-Request-Id": "1"})["builder"], "Wix")
        self.assertEqual(self.detect("<html><p>Hello</p></html>")["kind"], "unknown")


class VideoAndLlmsTests(SimpleTestCase):
    def video(self, html):
        checks, _ = audit_html("https://pelda.hu/", {}, GOOD_PAGE.replace(b"</body>", html + b"</body>"))
        return next(check for check in checks if check["id"] == "video")

    def test_no_video_is_only_information(self):
        checks, _ = audit_html("https://pelda.hu/", {}, GOOD_PAGE)
        video = next(check for check in checks if check["id"] == "video")
        self.assertEqual((video["status"], video["data"]["count"]), ("info", 0))

    def test_only_mp4_is_a_hint(self):
        check = self.video(b'<video src="/hero.mp4"></video>')
        self.assertEqual((check["status"], check["data"]["formats"]), ("warn", ["mp4"]))

    def test_webm_with_an_hevc_or_mp4_fallback_passes(self):
        check = self.video(
            b'<video><source src="/hero.webm" type="video/webm">'
            b'<source src="/hero.mp4" type=\'video/mp4; codecs="hvc1"\'></video>'
        )
        self.assertEqual((check["status"], check["data"]["formats"]), ("pass", ["hevc", "mp4", "webm"]))

    def test_automatic_format_and_script_added_sources(self):
        auto = self.video(b'<video src="https://res.cloudinary.com/x/video/upload/f_auto,q_auto/hero"></video>')
        self.assertEqual(auto["status"], "pass")
        scripted = self.video(b'<video muted poster="/p.jpg"></video>')
        self.assertEqual((scripted["status"], scripted["data"]["scripted"]), ("info", 1))

    @mock.patch("sitecheck.seo_audit.safe_get")
    def test_llms_txt_is_found_only_as_a_markdown_file(self, get):
        def fake(answer):
            def inner(url, **_kwargs):
                if url.endswith("/llms.txt"):
                    return url, 200, answer[0], answer[1]
                return url, 404, {}, b""

            return inner

        from .seo_audit import _site_files

        get.side_effect = fake(({"Content-Type": "text/plain"}, b"# Pelda Kft.\n> Webshop"))
        self.assertEqual(_site_files("https://pelda.hu/")[2]["status"], "pass")
        # A site answering every address with its HTML home page has no llms.txt.
        get.side_effect = fake(({"Content-Type": "text/html"}, b"<!doctype html>"))
        self.assertEqual(_site_files("https://pelda.hu/")[2]["status"], "info")


class PrivacyAuditTests(SimpleTestCase):
    def audit(self, html, platform=None, headers=None):
        from .privacy_audit import privacy_audit

        return {item["id"]: item for item in privacy_audit(html, headers or {}, platform)}

    def test_trackers_without_a_consent_tool_fail(self):
        result = self.audit(
            '<script async src="https://www.googletagmanager.com/gtag/js?id=G-ABC123"></script>'
            "<script>fbq('init', '123');</script>"
        )
        self.assertEqual(result["trackers"]["data"]["tracking"], ["Google Analytics", "Meta Pixel"])
        self.assertEqual(result["consent"]["status"], "fail")

    def test_a_consent_tool_or_consent_mode_passes(self):
        for extra in (
            '<script src="https://consent.cookiebot.com/uc.js"></script>',
            "<script>gtag('consent', 'default', {ad_storage: 'denied'});</script>",
            '<div id="cookie-banner">Sütik</div>',
        ):
            with self.subTest(extra=extra[:30]):
                result = self.audit('<script src="https://connect.facebook.net/en_US/fbevents.js"></script>' + extra)
                self.assertEqual(result["consent"]["status"], "pass")

    def test_cookieless_measurement_needs_no_consent(self):
        result = self.audit('<script src="/_vercel/insights/script.js"></script>')
        self.assertEqual(result["trackers"]["data"], {"tracking": [], "cookieless": ["Vercel Analytics"], "serverCookies": 0})
        self.assertEqual((result["consent"]["status"], result["cookiePolicy"]["status"]), ("pass", "info"))

    def test_a_plain_maps_link_is_not_an_embed(self):
        result = self.audit('<a href="https://maps.google.com/maps?q=Sopron">Térkép</a>')
        self.assertEqual(result["trackers"]["data"]["tracking"], [])
        embed = self.audit('<iframe src="https://www.google.com/maps?q=Sopron&output=embed"></iframe>')
        self.assertEqual(embed["trackers"]["data"]["tracking"], ["Google Maps"])
        # An embed without consent is a hint, not an error.
        self.assertEqual((embed["consent"]["status"], embed["consent"]["data"]["embedsOnly"]), ("warn", True))

    def test_legal_pages_are_found_by_link_or_text(self):
        result = self.audit(
            '<a href="/adatkezeles">Adatvédelem</a><a href="/impresszum">Impresszum</a>'
            '<a href="/aszf">ÁSZF</a><a href="/suti">Süti tájékoztató</a>'
        )
        self.assertEqual(
            [result[key]["status"] for key in ("privacyPolicy", "imprint", "terms", "cookiePolicy")],
            ["pass", "pass", "pass", "pass"],
        )

    def test_missing_legal_pages(self):
        result = self.audit('<a href="/rolunk">Rólunk</a><a href="/magbe">Magbe</a>')
        self.assertEqual(result["privacyPolicy"]["status"], "fail")
        self.assertEqual(result["imprint"]["status"], "warn")
        self.assertEqual(result["terms"]["status"], "info")
        shop = self.audit("<p>Bolt</p>", platform={"builder": "WordPress", "addons": ["WooCommerce"]})
        self.assertEqual(shop["terms"]["status"], "warn")


class ScreenshotTests(SimpleTestCase):
    def test_keeps_valid_images_and_spreads_the_filmstrip(self):
        from .screenshots import MAX_FRAMES, screenshots

        jpeg = "data:image/jpeg;base64,AAAA"
        lighthouse = {
            "audits": {
                "screenshot-thumbnails": {
                    "details": {"items": [{"timing": 300 * n, "data": jpeg} for n in range(1, 11)]}
                },
                "final-screenshot": {"details": {"data": "javascript:alert(1)"}},
            }
        }

        result = screenshots(lighthouse)

        self.assertEqual(len(result["filmstrip"]), MAX_FRAMES)
        self.assertEqual((result["filmstrip"][0]["timing"], result["filmstrip"][-1]["timing"]), (300, 3000))
        # Not an image data URI: replaced by the last frame.
        self.assertEqual(result["final"], jpeg)

    def test_no_report_data_gives_nothing(self):
        from .screenshots import screenshots

        self.assertEqual(screenshots({}), {"final": None, "filmstrip": []})


# A page built in the browser: the HTML is an empty shell, the bundle loads
# the tracking codes after consent and draws the banner.
SPA_SHELL = (
    '<!doctype html><html><head><script type="module" src="/assets/index-abc.js"></script>'
    '<link rel="modulepreload" href="/assets/vendor-def.js">'
    '<script src="https://cdn.example.com/lib.js"></script></head>'
    '<body><div id="root"></div></body></html>'
)
SPA_BUNDLE = (
    'const s=document.createElement("script");s.src="https://www.googletagmanager.com/gtag/js?id="+e;'
    'gtag("config","G-XYZ123");(function(c,l,a,r,i,t,y){t.src="https://www.clarity.ms/tag/"+i})();'
    '!function(f){f.src="https://connect.facebook.net/en_US/fbevents.js"}();'
    'jsx("div",{className:"fixed bottom-4 rounded-xl",children:[jsx("h2",{children:"Sütik és mérés"}),'
    'jsx("button",{children:"Elfogadom"}),jsx("button",{children:"Elutasítom"}),'
    'jsx(Link,{to:"/adatkezeles",children:"adatkezelési tájékoztató"})]});'
)


class PageScriptsTests(SimpleTestCase):
    def test_only_the_sites_own_scripts_are_read(self):
        from .page_scripts import script_urls

        self.assertEqual(
            script_urls("https://www.pelda.hu/", SPA_SHELL),
            ["https://www.pelda.hu/assets/index-abc.js", "https://www.pelda.hu/assets/vendor-def.js"],
        )

    @mock.patch("sitecheck.page_scripts.safe_get")
    def test_fetch_joins_the_files_and_skips_failures(self, get):
        from .page_scripts import fetch_page_scripts

        def fake(url, **_kwargs):
            if url.endswith("index-abc.js"):
                return url, 200, {}, b"first"
            raise FetchError("unreachable")

        get.side_effect = fake
        self.assertEqual(fetch_page_scripts("https://pelda.hu/", SPA_SHELL).strip(), "first")


class PrivacyFromScriptsTests(SimpleTestCase):
    def audit(self, html, scripts=""):
        from .privacy_audit import privacy_audit

        return {item["id"]: item for item in privacy_audit(html, {}, None, scripts)}

    def test_trackers_and_banner_in_the_bundle_are_found(self):
        result = self.audit(SPA_SHELL, SPA_BUNDLE)
        self.assertEqual(
            result["trackers"]["data"]["tracking"],
            ["Google Analytics", "Meta Pixel", "Microsoft Clarity"],
        )
        self.assertEqual(result["consent"]["status"], "pass")
        self.assertEqual(result["privacyPolicy"]["status"], "pass")
        # No separate cookie notice, but a privacy notice: a hint only.
        self.assertEqual(result["cookiePolicy"]["status"], "info")
        self.assertTrue(result["cookiePolicy"]["data"]["inPrivacy"])

    def test_the_shell_alone_shows_nothing(self):
        result = self.audit(SPA_SHELL)
        self.assertEqual(result["trackers"]["data"]["tracking"], [])

    def test_a_stored_consent_choice_counts_as_a_banner(self):
        bundle = 'localStorage.getItem("cookie-consent");s.src="https://connect.facebook.net/x.js"'
        self.assertEqual(self.audit(SPA_SHELL, bundle)["consent"]["status"], "pass")

    def test_a_tracker_without_any_banner_still_fails(self):
        bundle = 's.src="https://connect.facebook.net/x.js"'
        self.assertEqual(self.audit(SPA_SHELL, bundle)["consent"]["status"], "fail")

    def test_gtag_with_the_id_in_a_variable(self):
        bundle = 's.src="https://www.googletagmanager.com/gtag/js?id="+id'
        self.assertEqual(self.audit(SPA_SHELL, bundle)["trackers"]["data"]["tracking"], ["Google tag (gtag.js)"])
