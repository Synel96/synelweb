"""Tracking, cookie consent and the legal pages, read from a page's HTML.

Not legal advice: it reports what the source code shows (known tracking
scripts, a known consent tool, links to a privacy notice / imprint /
terms), and the site says so.
"""

import re

# (name, needles in the lowercased HTML, sets cookies?)
TRACKERS = (
    ("Google Analytics", ("googletagmanager.com/gtag/js?id=g-", "google-analytics.com/analytics.js", "gtag('config', 'g-", 'gtag("config", "g-', "google-analytics.com/ga.js"), True),
    ("Google Tag Manager", ("googletagmanager.com/gtm.js", "googletagmanager.com/ns.html"), True),
    ("Google Ads", ("googletagmanager.com/gtag/js?id=aw-", "gtag('config', 'aw-", 'gtag("config", "aw-', "googleadservices.com"), True),
    ("Meta Pixel", ("connect.facebook.net", "fbq('init'", 'fbq("init"'), True),
    ("TikTok Pixel", ("analytics.tiktok.com",), True),
    ("LinkedIn Insight", ("snap.licdn.com",), True),
    ("Microsoft Ads (UET)", ("bat.bing.com",), True),
    ("Microsoft Clarity", ("clarity.ms",), True),
    ("Hotjar", ("static.hotjar.com", "hotjar.com/c/hotjar"), True),
    ("Pinterest Tag", ("s.pinimg.com/ct/",), True),
    ("X (Twitter) Pixel", ("static.ads-twitter.com",), True),
    ("Yandex Metrica", ("mc.yandex.ru", "mc.yandex.com"), True),
    ("Smartlook", ("smartlook.com",), True),
    ("Matomo", ("matomo.js", "piwik.js"), True),
    ("YouTube", ("youtube.com/embed/",), True),
    # Only an embedded map loads Google's code; a plain link to Maps doesn't.
    ("Google Maps", ("google.com/maps/embed", "output=embed"), True),
    # Cookieless measurement: no consent needed for these.
    ("Vercel Analytics", ("/_vercel/insights", "va.vercel-scripts.com"), False),
    ("Plausible", ("plausible.io/js",), False),
    ("Fathom", ("cdn.usefathom.com",), False),
    ("YouTube (nocookie)", ("youtube-nocookie.com/embed/",), False),
)

# Embedded content rather than tracking: still sets third-party cookies, but
# a lesser issue than analytics / ad pixels without consent.
EMBEDS = {"YouTube", "Google Maps"}

# Known consent tools (CMPs) and their usual traces.
CONSENT_TOOLS = (
    ("Cookiebot", ("consent.cookiebot.com", "cookiebot")),
    ("CookieYes", ("cdn-cookieyes.com", "cookieyes")),
    ("OneTrust", ("cdn.cookielaw.org", "onetrust")),
    ("Usercentrics", ("usercentrics",)),
    ("Complianz", ("complianz",)),
    ("Borlabs Cookie", ("borlabs-cookie",)),
    ("CookieAdmin / GDPR Cookie Consent", ("cookie-law-info", "cookielawinfo")),
    ("Cookie Notice", ("cookie-notice",)),
    ("Real Cookie Banner", ("real-cookie-banner",)),
    ("Iubenda", ("iubenda",)),
    ("Termly", ("termly.io",)),
    ("Osano", ("osano.com",)),
    ("CookieFirst", ("cookiefirst",)),
    ("Klaro", ("klaro",)),
    ("Cookie Consent", ("cookieconsent", "cookie-consent", "cc-banner", "cc_banner")),
    ("Moove GDPR", ("moove_gdpr", "moove-gdpr")),
)
# Google Consent Mode: tags wait for consent.
CONSENT_MODE = re.compile(r"""gtag\(\s*['"]consent['"]\s*,\s*['"]default['"]""")
# A home-made banner: an element whose id/class says cookie banner/consent.
GENERIC_BANNER = re.compile(r"""(?:id|class)=["'][^"']*cookie[-_ ]?(?:banner|consent|notice|bar|popup)""")

LEGAL_LINKS = {
    "privacyPolicy": ("adatkezel", "adatvédel", "adatvedel", "privacy", "datenschutz", "gdpr"),
    "imprint": ("impresszum", "impressum", "imprint", "legal notice", "cégadatok", "cegadatok"),
    "terms": ("ászf", "aszf", "általános szerződési", "altalanos-szerzodesi", "terms", "agb", "felhasználási feltételek", "felhasznalasi-feltetelek", "geschäftsbedingungen"),
    "cookiePolicy": ("süti", "suti", "cookie-policy", "cookie policy", "cookie-szabályzat", "cookie tájékoztató", "cookie-richtlinie"),
}
SHOP_BUILDERS = {"Shopify", "UNAS", "Shoprenter", "PrestaShop", "Magento"}
_LINK = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.S | re.I)
_HREF = re.compile(r"""href\s*=\s*["']([^"']*)["']""", re.I)
_TAGS = re.compile(r"<[^>]+>")


def _links(html):
    """(href, visible text) of every link, lowercased."""
    for attributes, inner in _LINK.findall(html):
        href = (_HREF.search(attributes) or [None, ""])[1]
        yield href.lower(), _TAGS.sub(" ", inner).lower()


def privacy_audit(html, headers, platform):
    lowered = html.lower()
    trackers = [(name, sets_cookies) for name, needles, sets_cookies in TRACKERS if any(n in lowered for n in needles)]
    cookie_trackers = [name for name, sets_cookies in trackers if sets_cookies]
    cookieless = [name for name, sets_cookies in trackers if not sets_cookies]

    tools = [name for name, needles in CONSENT_TOOLS if any(n in lowered for n in needles)]
    consent_mode = bool(CONSENT_MODE.search(lowered))
    generic_banner = bool(GENERIC_BANNER.search(lowered))
    has_consent = bool(tools) or consent_mode or generic_banner

    set_cookie = [v for k, v in headers.items() if k.lower() == "set-cookie"]

    tracking_pixels = [name for name in cookie_trackers if name not in EMBEDS]
    if not cookie_trackers or has_consent:
        consent_status = "pass"
    else:
        # Analytics / ad pixels without any consent tool: a real risk. Only
        # embeds (a map, a video): worth a click-to-load, not an alarm.
        consent_status = "fail" if tracking_pixels else "warn"

    links = list(_links(html))

    def contains(haystack, needle):
        # Short needles (ászf, agb, gdpr) only as whole words.
        if len(needle) <= 4:
            return re.search(rf"(?<![a-zá-ű]){re.escape(needle)}(?![a-zá-ű])", haystack) is not None
        return needle in haystack

    def has_link(key):
        needles = LEGAL_LINKS[key]
        return any(
            any(contains(href, needle) or contains(text, needle) for needle in needles)
            for href, text in links
        )

    is_shop = bool(platform and ("WooCommerce" in platform.get("addons", []) or platform.get("builder") in SHOP_BUILDERS))
    found = {key: has_link(key) for key in LEGAL_LINKS}

    return [
        {
            "id": "trackers",
            "status": "info",
            "data": {"tracking": cookie_trackers, "cookieless": cookieless, "serverCookies": len(set_cookie)},
        },
        {
            "id": "consent",
            "status": consent_status,
            "data": {
                "tools": tools[:3],
                "consentMode": consent_mode,
                "tracking": len(cookie_trackers),
                "embedsOnly": bool(cookie_trackers) and not tracking_pixels,
                "found": has_consent,
            },
        },
        {"id": "privacyPolicy", "status": "pass" if found["privacyPolicy"] else "fail", "data": {}},
        {"id": "imprint", "status": "pass" if found["imprint"] else "warn", "data": {}},
        {
            "id": "terms",
            "status": "pass" if found["terms"] else ("warn" if is_shop else "info"),
            "data": {"shop": is_shop},
        },
        {
            "id": "cookiePolicy",
            "status": "pass" if found["cookiePolicy"] else ("warn" if cookie_trackers else "info"),
            "data": {},
        },
    ]
