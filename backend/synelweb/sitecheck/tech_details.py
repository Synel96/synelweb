"""Technical details from the Lighthouse report, YellowLab Tools style.

Read from the same PageSpeed response the scores come from (no extra
request): fonts, JavaScript and CSS weight, code splitting, caching, page
weight, DOM size, third parties. Each item is {"id", "status", "data"}
like the SEO checks; the texts live in the frontend.
"""

KB = 1024


def _audit(audits, *ids):
    """The first of the given audits the report has (names changed between
    Lighthouse versions, e.g. uses-long-cache-ttl -> cache-insight)."""
    for audit_id in ids:
        audit = audits.get(audit_id)
        if audit and audit.get("scoreDisplayMode") not in ("error", "notApplicable"):
            return audit
    return {}


def _items(audit):
    return ((audit or {}).get("details") or {}).get("items") or []


def _savings_bytes(audit):
    details = (audit or {}).get("details") or {}
    return details.get("overallSavingsBytes") or 0


def _kb(value):
    return round((value or 0) / KB)


def _grade(value, warn, fail):
    if value >= fail:
        return "fail"
    return "warn" if value >= warn else "pass"


def tech_details(audits):
    requests = _items(audits.get("network-requests"))
    if not requests:
        return []

    by_type = {}
    for request in requests:
        kind = request.get("resourceType") or "Other"
        size = request.get("transferSize") or 0
        entry = by_type.setdefault(kind, {"count": 0, "bytes": 0, "largest": 0})
        entry["count"] += 1
        entry["bytes"] += size
        entry["largest"] = max(entry["largest"], size)

    fonts = by_type.get("Font", {"count": 0, "bytes": 0})
    scripts = by_type.get("Script", {"count": 0, "bytes": 0, "largest": 0})
    styles = by_type.get("Stylesheet", {"count": 0, "bytes": 0})
    total_bytes = (audits.get("total-byte-weight") or {}).get("numericValue") or sum(
        entry["bytes"] for entry in by_type.values()
    )

    font_display = _audit(audits, "font-display", "font-display-insight")
    font_status = _grade(fonts["count"], 5, 9)
    if font_status == "pass" and font_display and (font_display.get("score") or 1) < 0.9:
        font_status = "warn"

    unused_js = _savings_bytes(_audit(audits, "unused-javascript"))
    js_status = max(
        _grade(_kb(scripts["bytes"]), 500, 1000),
        _grade(_kb(unused_js), 150, 400),
        key=("pass", "warn", "fail").index,
    )
    # One big bundle loaded up front: the code isn't split per page.
    largest_js = _kb(scripts.get("largest", 0))
    splitting_status = _grade(largest_js, 300, 600) if scripts["count"] else "pass"

    unused_css = _savings_bytes(_audit(audits, "unused-css-rules"))

    cache_audit = _audit(audits, "uses-long-cache-ttl", "cache-insight")
    short_cache = len(_items(cache_audit))

    dom_audit = _audit(audits, "dom-size", "dom-size-insight")
    dom_nodes = round(dom_audit.get("numericValue") or 0)

    third_party = _audit(audits, "third-party-summary", "third-parties-insight")
    third_parties = len(_items(third_party))

    compression = _savings_bytes(_audit(audits, "uses-text-compression"))
    image_savings = _savings_bytes(_audit(audits, "modern-image-formats")) + _savings_bytes(
        _audit(audits, "uses-optimized-images")
    )

    details = [
        {
            "id": "pageWeight",
            "status": _grade(_kb(total_bytes), 1500, 3000),
            "data": {"kb": _kb(total_bytes), "requests": len(requests)},
        },
        {
            "id": "fonts",
            "status": font_status,
            "data": {"count": fonts["count"], "kb": _kb(fonts["bytes"])},
        },
        {
            "id": "javascript",
            "status": js_status,
            "data": {
                "count": scripts["count"],
                "kb": _kb(scripts["bytes"]),
                "unusedKb": _kb(unused_js),
            },
        },
        {
            "id": "codeSplitting",
            "status": splitting_status,
            "data": {"largestKb": largest_js},
        },
        {
            "id": "css",
            "status": _grade(_kb(unused_css), 50, 150),
            "data": {"count": styles["count"], "kb": _kb(styles["bytes"]), "unusedKb": _kb(unused_css)},
        },
        {
            "id": "cache",
            "status": "pass" if short_cache == 0 else ("warn" if short_cache < 10 else "fail"),
            "data": {"shortCache": short_cache},
        },
        {
            "id": "domSize",
            "status": _grade(dom_nodes, 1500, 3000) if dom_nodes else "info",
            "data": {"nodes": dom_nodes},
        },
        {
            "id": "thirdParty",
            "status": _grade(third_parties, 6, 12),
            "data": {"count": third_parties},
        },
        {
            "id": "compression",
            "status": "warn" if _kb(compression) >= 10 else "pass",
            "data": {"savingsKb": _kb(compression)},
        },
        {
            "id": "imageFormats",
            "status": _grade(_kb(image_savings), 100, 500),
            "data": {"savingsKb": _kb(image_savings)},
        },
    ]
    return details
