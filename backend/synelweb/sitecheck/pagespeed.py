"""Google PageSpeed Insights: run a Lighthouse check and keep what the page shows.

The API key (PAGESPEED_API_KEY) is optional: without it Google serves the
request from a small shared quota and often answers 429.
"""

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
CATEGORIES = ("performance", "accessibility", "best-practices", "seo")
LAB_METRICS = (
    "first-contentful-paint",
    "largest-contentful-paint",
    "total-blocking-time",
    "cumulative-layout-shift",
    "speed-index",
)
FIELD_METRICS = {
    "LARGEST_CONTENTFUL_PAINT_MS": "lcp",
    "INTERACTION_TO_NEXT_PAINT": "inp",
    "CUMULATIVE_LAYOUT_SHIFT_SCORE": "cls",
}
MAX_OPPORTUNITIES = 5


class PageSpeedError(Exception):
    """code: 'unreachable' (Lighthouse couldn't load the page), 'quota', or 'upstream'."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _score(category):
    value = (category or {}).get("score")
    return None if value is None else round(value * 100)


def _summarise(data):
    lighthouse = data.get("lighthouseResult") or {}
    categories = lighthouse.get("categories") or {}
    audits = lighthouse.get("audits") or {}

    scores = {
        "performance": _score(categories.get("performance")),
        "accessibility": _score(categories.get("accessibility")),
        "bestPractices": _score(categories.get("best-practices")),
        "seo": _score(categories.get("seo")),
    }

    lab = []
    for key in LAB_METRICS:
        audit = audits.get(key)
        if not audit:
            continue
        lab.append(
            {
                "id": key,
                "title": audit.get("title", ""),
                "value": audit.get("displayValue", ""),
                "score": audit.get("score"),
            }
        )

    # Real-user data (Chrome UX Report); only for sites with enough traffic.
    field = []
    for key, short in FIELD_METRICS.items():
        metric = ((data.get("loadingExperience") or {}).get("metrics") or {}).get(key)
        if metric:
            field.append(
                {
                    "id": short,
                    "percentile": metric.get("percentile"),
                    "category": metric.get("category", ""),
                }
            )

    # The biggest wins: the performance audits Lighthouse says would save
    # time or layout shift. Older Lighthouse reports them as "opportunity"
    # audits with overallSavingsMs; newer ones as insights with
    # metricSavings (LCP/FCP/TBT in ms, CLS as a score), so read both.
    perf_ids = [
        ref.get("id")
        for ref in (categories.get("performance") or {}).get("auditRefs") or []
        if ref.get("group") != "metrics"
    ] or list(audits)
    opportunities = []
    seen_titles = set()
    for audit_id in perf_ids:
        audit = audits.get(audit_id) or {}
        if audit.get("scoreDisplayMode") in ("notApplicable", "informative", "manual", "error"):
            continue
        score = audit.get("score")
        if score is not None and score >= 0.9:
            continue
        details = audit.get("details") or {}
        metric_savings = audit.get("metricSavings") or {}
        savings_ms = max(
            details.get("overallSavingsMs") or 0,
            *(metric_savings.get(key) or 0 for key in ("LCP", "FCP", "TBT", "INP")),
        )
        cls_savings = metric_savings.get("CLS") or 0
        title = audit.get("title", "")
        if (savings_ms <= 0 and cls_savings <= 0) or not title or title in seen_titles:
            continue
        seen_titles.add(title)
        opportunities.append(
            {
                "id": audit.get("id", audit_id),
                "title": title,
                "savingsMs": round(savings_ms),
                "clsSavings": round(cls_savings, 3),
                "value": audit.get("displayValue", ""),
            }
        )
    # A CLS saving of 0.1 weighs about as much as a second of loading time.
    opportunities.sort(
        key=lambda item: item["savingsMs"] + item["clsSavings"] * 10000, reverse=True
    )

    return {
        "finalUrl": lighthouse.get("finalDisplayedUrl") or lighthouse.get("finalUrl") or "",
        "scores": scores,
        "lab": lab,
        "field": field,
        "opportunities": opportunities[:MAX_OPPORTUNITIES],
    }


def run_pagespeed(url, strategy, locale):
    params = [
        ("url", url),
        ("strategy", strategy),
        ("locale", locale),
        *[("category", category) for category in CATEGORIES],
    ]
    key = getattr(settings, "PAGESPEED_API_KEY", "")
    if key:
        params.append(("key", key))

    try:
        response = requests.get(ENDPOINT, params=params, timeout=settings.PAGESPEED_TIMEOUT)
    except requests.RequestException:
        logger.warning("PageSpeed request failed for %s", url, exc_info=True)
        raise PageSpeedError("upstream")

    if response.status_code == 429:
        raise PageSpeedError("quota")
    if response.status_code == 400:
        # Lighthouse could not load the page (DNS, timeout, error status…).
        raise PageSpeedError("unreachable")
    if not response.ok:
        logger.warning("PageSpeed answered %s for %s", response.status_code, url)
        raise PageSpeedError("upstream")

    return _summarise(response.json())
