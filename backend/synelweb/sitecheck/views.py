import hashlib

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .models import SiteCheck
from .pagespeed import PageSpeedError, run_pagespeed
from .serializers import SiteCheckRequestSerializer

CACHE_SECONDS = 30 * 60
ERROR_STATUS = {
    "unreachable": status.HTTP_422_UNPROCESSABLE_ENTITY,
    "quota": status.HTTP_503_SERVICE_UNAVAILABLE,
    "upstream": status.HTTP_502_BAD_GATEWAY,
}


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
            try:
                result = run_pagespeed(url, strategy, lang)
            except PageSpeedError as error:
                return Response({"error": error.code}, status=ERROR_STATUS[error.code])
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
