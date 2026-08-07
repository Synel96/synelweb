"""Trigger a Vercel deploy hook whenever admin-editable content changes.

The frontend is a statically prerendered site: services, reviews and blog
posts are baked into the build at deploy time. Without this, an admin
approving a review or publishing a new service/blog post would not show up
on the live site until someone manually redeployed. Wiring this into the
Django signals (see `core/signals.py`) means any add/edit/delete of that
content kicks off a fresh Vercel build automatically.
"""

import logging
import threading
import time

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

_DEBOUNCE_CACHE_KEY = "vercel_deploy_hook:last_triggered"


def trigger_vercel_deploy(reason):
    """Fire the configured Vercel deploy hook, debounced, on a background thread.

    Safe to call from request/admin code: never raises, and never blocks the
    caller on the network request.
    """
    hook_url = getattr(settings, "VERCEL_DEPLOY_HOOK_URL", "")
    if not hook_url:
        logger.debug("VERCEL_DEPLOY_HOOK_URL not set; skipping deploy trigger for %s", reason)
        return

    debounce_seconds = getattr(settings, "VERCEL_DEPLOY_HOOK_DEBOUNCE_SECONDS", 30)
    # cache.add only succeeds if the key isn't already set, so this doubles as a lock:
    # rapid-fire saves (e.g. bulk review approval) collapse into a single deploy.
    if debounce_seconds > 0 and not cache.add(_DEBOUNCE_CACHE_KEY, True, timeout=debounce_seconds):
        logger.info("Skipping Vercel deploy trigger for %s: triggered within the last %ss", reason, debounce_seconds)
        return

    thread = threading.Thread(target=_send_deploy_hook, args=(hook_url, reason), daemon=True)
    thread.start()


def _send_deploy_hook(hook_url, reason):
    started = time.monotonic()
    try:
        response = requests.post(hook_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        logger.exception("Vercel deploy hook request failed (reason=%s)", reason)
        return
    logger.info(
        "Triggered Vercel deploy (reason=%s, status=%s, took=%.2fs)",
        reason,
        response.status_code,
        time.monotonic() - started,
    )
