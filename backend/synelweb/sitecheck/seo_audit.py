"""SEO basics of a page, read from its HTML: what Lighthouse doesn't check.

Each check is {"id", "status", "data"}: status is "pass", "warn", "fail" or
"info", and data holds the numbers the site needs to explain it. The texts
live in the frontend (three languages).
"""

import json
import logging
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

from .safe_fetch import FetchError, safe_get

logger = logging.getLogger(__name__)

TITLE_RANGE = (30, 60)
DESCRIPTION_RANGE = (70, 160)
# Less visible text than this, with scripts on the page: the content is
# probably built in the browser, so the raw HTML can't tell the whole story.
CLIENT_RENDERED_TEXT = 200
# Types that tell search engines who runs the site.
BUSINESS_TYPES = {
    "organization",
    "localbusiness",
    "professionalservice",
    "corporation",
    "store",
    "onlinestore",
    "restaurant",
    "dentist",
    "medicalbusiness",
    "legalservice",
    "homeandconstructionbusiness",
    "automotivebusiness",
    "healthandbeautybusiness",
    "lodgingbusiness",
    "foodestablishment",
    "person",
}
MAX_TYPES = 12


class _PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.title = None
        self._in_title = False
        self.meta = {}
        self.canonical = ""
        self.hreflangs = []
        self.h1 = 0
        self.images = 0
        self.images_without_alt = 0
        self.json_ld = []
        self._json_ld_buffer = None
        self.microdata_types = []
        self.scripts = 0
        self._skip_depth = 0
        self.text_chars = 0

    def handle_starttag(self, tag, attrs):
        attributes = {name.lower(): (value or "") for name, value in attrs}
        if tag == "html" and not self.lang:
            self.lang = attributes.get("lang", "").strip()
        elif tag == "title" and self.title is None:
            self._in_title = True
            self.title = ""
        elif tag == "meta":
            key = (attributes.get("name") or attributes.get("property") or "").strip().lower()
            if key and key not in self.meta:
                self.meta[key] = attributes.get("content", "").strip()
        elif tag == "link":
            rel = attributes.get("rel", "").lower().split()
            if "canonical" in rel and not self.canonical:
                self.canonical = attributes.get("href", "").strip()
            if "alternate" in rel and attributes.get("hreflang"):
                self.hreflangs.append(attributes["hreflang"].strip())
        elif tag == "h1":
            self.h1 += 1
        elif tag == "img":
            self.images += 1
            if "alt" not in attributes:
                self.images_without_alt += 1
        elif tag == "script":
            self.scripts += 1
            if attributes.get("type", "").strip().lower() == "application/ld+json":
                self._json_ld_buffer = []
            self._skip_depth += 1
        elif tag in ("style", "noscript", "template"):
            self._skip_depth += 1
        if attributes.get("itemtype"):
            self.microdata_types.append(attributes["itemtype"].rstrip("/").rsplit("/", 1)[-1])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            if self._json_ld_buffer is not None:
                self.json_ld.append("".join(self._json_ld_buffer))
                self._json_ld_buffer = None
            self._skip_depth = max(0, self._skip_depth - 1)
        elif tag in ("style", "noscript", "template"):
            self._skip_depth = max(0, self._skip_depth - 1)

    def handle_data(self, data):
        if self._json_ld_buffer is not None:
            self._json_ld_buffer.append(data)
        elif self._in_title:
            self.title += data
        elif not self._skip_depth:
            self.text_chars += len(data.strip())


def _json_ld_types(blocks):
    """(types, invalid block count) of the page's JSON-LD.

    Only the top-level things (and the items of an @graph) count: the nested
    ones (an address, a FAQ's answers) are parts of those, not separate data.
    """
    types = []
    invalid = 0

    def add(node):
        if not isinstance(node, dict):
            return
        kind = node.get("@type")
        for name in kind if isinstance(kind, list) else [kind]:
            if isinstance(name, str) and name and name not in types:
                types.append(name)

    def collect(node):
        if isinstance(node, list):
            for item in node:
                collect(item)
        elif isinstance(node, dict):
            add(node)
            graph = node.get("@graph")
            if isinstance(graph, list):
                for item in graph:
                    add(item)

    for block in blocks:
        try:
            collect(json.loads(block))
        except ValueError:
            invalid += 1
    return types, invalid


def _length_status(text, low, high):
    if not text:
        return "fail"
    return "pass" if low <= len(text) <= high else "warn"


def _robots_blocks_all(robots_txt):
    """Disallow: / for every crawler (User-agent: *)."""
    applies = False
    for raw in robots_txt.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, value = (part.strip() for part in line.split(":", 1))
        field = field.lower()
        if field == "user-agent":
            applies = value == "*"
        elif field == "disallow" and applies and value == "/":
            return True
    return False


def _site_files(final_url):
    """robots.txt and sitemap of the site's origin, as two checks."""
    parts = urlsplit(final_url)
    origin = f"{parts.scheme}://{parts.netloc}"
    robots = {"id": "robots", "status": "warn", "data": {}}
    sitemaps = []
    try:
        _, status, _, body = safe_get(f"{origin}/robots.txt", max_bytes=200_000, accept="text/plain")
        if status == 200:
            text = body.decode("utf-8", "replace")
            robots = {
                "id": "robots",
                "status": "fail" if _robots_blocks_all(text) else "pass",
                "data": {"blocksAll": _robots_blocks_all(text)},
            }
            sitemaps = [
                line.split(":", 1)[1].strip()
                for line in text.splitlines()
                if line.lower().startswith("sitemap:")
            ]
    except FetchError:
        pass

    sitemap = {"id": "sitemap", "status": "warn", "data": {"inRobots": bool(sitemaps)}}
    for candidate in [*sitemaps[:2], f"{origin}/sitemap.xml"]:
        try:
            _, status, _, body = safe_get(
                urljoin(origin, candidate), max_bytes=50_000, accept="application/xml,text/xml"
            )
        except FetchError:
            continue
        if status == 200 and b"<" in body[:2000]:
            sitemap = {"id": "sitemap", "status": "pass", "data": {"inRobots": bool(sitemaps)}}
            break
    return [robots, sitemap]


def audit_html(final_url, headers, body):
    """The checks for one fetched page (no network: robots/sitemap are separate)."""
    parser = _PageParser()
    try:
        parser.feed(body.decode("utf-8", "replace"))
        parser.close()
    except Exception:  # noqa: BLE001 - malformed HTML still gives partial results
        logger.info("HTML parse stopped early for %s", final_url, exc_info=True)

    types, invalid = _json_ld_types(parser.json_ld)
    for name in parser.microdata_types:
        if name and name not in types:
            types.append(name)
    has_business = any(name.lower() in BUSINESS_TYPES for name in types)
    if not types:
        structured = "fail" if invalid else "warn"
    else:
        structured = "pass" if has_business and not invalid else "warn"

    title = re.sub(r"\s+", " ", parser.title or "").strip()
    description = parser.meta.get("description", "")
    robots_meta = (parser.meta.get("robots", "") + "," + parser.meta.get("googlebot", "")).lower()
    header_robots = str({k.lower(): v for k, v in headers.items()}.get("x-robots-tag", "")).lower()
    noindex = "noindex" in robots_meta or "noindex" in header_robots
    og_present = [key for key in ("og:title", "og:image") if parser.meta.get(key)]

    checks = [
        {
            "id": "structuredData",
            "status": structured,
            "data": {"types": types[:MAX_TYPES], "invalid": invalid, "hasBusiness": has_business},
        },
        {"id": "title", "status": _length_status(title, *TITLE_RANGE), "data": {"length": len(title)}},
        {
            "id": "description",
            "status": _length_status(description, *DESCRIPTION_RANGE),
            "data": {"length": len(description)},
        },
        {
            "id": "h1",
            "status": "pass" if parser.h1 == 1 else ("fail" if parser.h1 == 0 else "warn"),
            "data": {"count": parser.h1},
        },
        {"id": "indexable", "status": "fail" if noindex else "pass", "data": {}},
        {"id": "canonical", "status": "pass" if parser.canonical else "warn", "data": {}},
        {"id": "viewport", "status": "pass" if parser.meta.get("viewport") else "fail", "data": {}},
        {"id": "lang", "status": "pass" if parser.lang else "warn", "data": {"lang": parser.lang[:12]}},
        {
            "id": "social",
            "status": "pass" if len(og_present) == 2 else "warn",
            "data": {"found": len(og_present)},
        },
        {
            "id": "hreflang",
            "status": "pass" if parser.hreflangs else "info",
            "data": {"count": len(set(parser.hreflangs))},
        },
        {
            "id": "images",
            "status": "warn" if parser.images_without_alt else "pass",
            "data": {"total": parser.images, "missingAlt": parser.images_without_alt},
        },
        {"id": "https", "status": "pass" if final_url.startswith("https://") else "fail", "data": {}},
    ]
    client_rendered = parser.text_chars < CLIENT_RENDERED_TEXT and parser.scripts > 0
    return checks, client_rendered


def run_seo_audit(url):
    """The SEO basics of a public page, or None when it can't be fetched."""
    try:
        final_url, status, headers, body = safe_get(url)
    except FetchError as error:
        logger.info("SEO audit could not fetch %s (%s)", url, error)
        return None
    if status >= 400:
        return None

    checks, client_rendered = audit_html(final_url, headers, body)
    checks += _site_files(final_url)
    return {"finalUrl": final_url, "checks": checks, "clientRendered": client_rendered}
