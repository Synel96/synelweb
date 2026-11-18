import hashlib
import logging
from concurrent.futures import ThreadPoolExecutor

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import SiteCheck
from .pagespeed import PageSpeedError, run_pagespeed
from .seo_audit import run_seo_audit
from .serializers import SiteCheckRequestSerializer

logger = logging.getLogger(__name__)

CACHE_SECONDS = 30 * 60
ERROR_STATUS = {
    "unreachable": status.HTTP_422_UNPROCESSABLE_ENTITY,
    "quota": status.HTTP_503_SERVICE_UNAVAILABLE,
    "upstream": status.HTTP_502_BAD_GATEWAY,
}


def _safe_seo_audit(url):
    try:
        return run_seo_audit(url)
    except Exception:  # noqa: BLE001 - an extra must never break the check
        logger.exception("SEO audit failed for %s", url)
        return None


class SiteCheckAPIView(APIView):
    """Runs a Lighthouse check of a public website through PageSpeed Insights."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "site_checks"
    # Public tool: no session auth, so no CSRF check.
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = SiteCheckRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data["url"]
        strategy = serializer.validated_data["strategy"]
        lang = serializer.validated_data["lang"]

        digest = hashlib.sha256(f"{url}|{strategy}|{lang}".encode()).hexdigest()
        cache_key = f"sitecheck:{digest}"
        result = cache.get(cache_key)
        if result is None:
            # The SEO basics read the page's HTML directly, alongside the
            # (much slower) Lighthouse run; they never fail the check.
            with ThreadPoolExecutor(max_workers=1) as pool:
                seo_future = pool.submit(_safe_seo_audit, url)
                try:
                    result = run_pagespeed(url, strategy, lang)
                except PageSpeedError as error:
                    return Response({"error": error.code}, status=ERROR_STATUS[error.code])
                result = {**result, "seo": seo_future.result()}
            cache.set(cache_key, result, CACHE_SECONDS)
            scores = result["scores"]
            SiteCheck.objects.create(
                url=url,
                strategy=strategy,
                site_language=lang,
                performance=scores["performance"],
                accessibility=scores["accessibility"],
                best_practices=scores["bestPractices"],
                seo=scores["seo"],
            )

        return Response({"url": url, "strategy": strategy, **result})
