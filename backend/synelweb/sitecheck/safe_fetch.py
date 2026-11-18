"""Fetch a page of a public website without letting the checker reach inside.

The URL comes from a visitor, so before every request (and every redirect
hop) the host must resolve only to public addresses, only http(s) on the
standard ports is allowed, and the response is cut at a size limit. This
keeps the tool from being used to probe the server's own network (SSRF).
"""

import ipaddress
import socket
from urllib.parse import urljoin, urlsplit

import requests

MAX_BYTES = 2 * 1024 * 1024
MAX_REDIRECTS = 5
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 10
USER_AGENT = "SynelWebSiteCheck/1.0 (+https://synelweb.hu/hu/weboldal-ellenorzes)"


class FetchError(Exception):
    pass


def _is_public_host(host, port):
    """Every address the host resolves to is a public one."""
    try:
        infos = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
    except (socket.gaierror, UnicodeError):
        return False
    if not infos:
        return False
    for info in infos:
        address = ipaddress.ip_address(info[4][0].split("%", 1)[0])
        if not address.is_global or address.is_multicast:
            return False
    return True


def _check_url(url):
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise FetchError("scheme")
    if parts.port not in (None, 80, 443):
        raise FetchError("port")
    if parts.username or parts.password:
        raise FetchError("credentials")
    port = parts.port or (443 if parts.scheme == "https" else 80)
    if not _is_public_host(parts.hostname, port):
        raise FetchError("not_public")


def safe_get(url, *, max_bytes=MAX_BYTES, accept="text/html,application/xhtml+xml"):
    """GET a public URL, following up to MAX_REDIRECTS redirects.

    Returns (final_url, status_code, headers, body_bytes). Raises FetchError
    when the address isn't allowed or the site can't be reached.
    """
    for _ in range(MAX_REDIRECTS + 1):
        _check_url(url)
        try:
            response = requests.get(
                url,
                stream=True,
                allow_redirects=False,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                headers={"User-Agent": USER_AGENT, "Accept": accept},
            )
        except requests.RequestException as error:
            raise FetchError("unreachable") from error

        try:
            if response.is_redirect and response.headers.get("Location"):
                url = urljoin(url, response.headers["Location"])
                continue

            body = bytearray()
            for chunk in response.iter_content(chunk_size=65536):
                body.extend(chunk)
                if len(body) >= max_bytes:
                    del body[max_bytes:]
                    break
            return url, response.status_code, dict(response.headers), bytes(body)
        except requests.RequestException as error:
            raise FetchError("unreachable") from error
        finally:
            response.close()

    raise FetchError("too_many_redirects")
