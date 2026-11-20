"""The site's own JavaScript files, for what the raw HTML doesn't show.

A page built in the browser (React, Vue, ...) often loads its tracking codes
and draws its cookie banner from its JavaScript bundle, so the HTML alone
says "no tracking, no banner". The privacy check reads these files too.
Only files on the site's own domain are fetched, through the same safe
fetch as the page itself, a few at a time and size-limited.
"""

import logging
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlsplit

from .safe_fetch import FetchError, safe_get

logger = logging.getLogger(__name__)

MAX_FILES = 6
MAX_FILE_BYTES = 3 * 1024 * 1024
_SCRIPT_SRC = re.compile(r"""<script\b[^>]*?\bsrc\s*=\s*["']([^"']+)["']""", re.I)
_PRELOAD = re.compile(r"""<link\b(?=[^>]*\brel\s*=\s*["'](?:modulepreload|preload)["'])[^>]*?\bhref\s*=\s*["']([^"']+\.m?js(?:\?[^"']*)?)["']""", re.I)


def _site_host(url):
    host = (urlsplit(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def script_urls(page_url, html):
    """The page's own script files (same domain, www or not), in order."""
    site = _site_host(page_url)
    urls = []
    for src in _SCRIPT_SRC.findall(html) + _PRELOAD.findall(html):
        url = urljoin(page_url, src.strip())
        if urlsplit(url).scheme in ("http", "https") and _site_host(url) == site and url not in urls:
            urls.append(url)
    return urls[:MAX_FILES]


def _fetch(url):
    try:
        _final, status, _headers, body = safe_get(url, max_bytes=MAX_FILE_BYTES, accept="*/*")
    except FetchError:
        return ""
    if status >= 400:
        return ""
    return body.decode("utf-8", "replace")


def fetch_page_scripts(page_url, html):
    """The text of the page's own script files, joined; "" when none."""
    urls = script_urls(page_url, html)
    if not urls:
        return ""
    try:
        with ThreadPoolExecutor(max_workers=3) as pool:
            return "\n".join(pool.map(_fetch, urls))
    except Exception:  # noqa: BLE001 - an extra must never break the check
        logger.exception("Could not read the scripts of %s", page_url)
        return ""
