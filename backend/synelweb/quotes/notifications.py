"""E-mail notification for a new quote request.

Sent only when both QUOTE_NOTIFY_EMAIL and an e-mail backend (EMAIL_HOST)
are configured; until then requests are still saved and listed in the admin.
Never raises and never blocks the request on the mail server.
"""

import logging
import threading

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def _body(quote):
    lines = [
        f"Űrlap: {quote.get_mode_display()}",
        f"Szolgáltatás: {quote.service_display()}",
        f"Név: {quote.name}",
        f"E-mail: {quote.email}",
        f"Telefon: {quote.phone or '-'}",
        f"Kapcsolatfelvétel: {quote.get_contact_preference_display() or '-'}",
        f"Oldal nyelve: {quote.site_language}",
        "",
        "Üzenet:",
        quote.message,
    ]
    if quote.is_bundle_request():
        # Right under the request, so the free setup isn't missed in the quote.
        lines[2:2] = [
            "Csomagakció: weboldal + Google Ads – a hirdetési fiók beállítása ingyenes",
        ]
    if quote.mode == quote.Mode.DETAILED and quote.is_ads_request():
        lines += [
            "",
            "Részletek (hirdetési kampány):",
            f"Google Ads fiók: {quote.get_ads_account_display() or '-'}",
            f"Weboldal: {quote.website_url or '-'}",
            f"Hirdetés nyelvei: {', '.join(quote.language_labels()) or '-'}",
            f"Havi hirdetési keret: {quote.get_ad_budget_display() or '-'}",
            f"Indulás: {quote.get_timeline_display() or '-'}",
            f"Sopron környéki: {'igen' if quote.is_local else 'nem'}",
        ]
    elif quote.mode == quote.Mode.DETAILED:
        lines += [
            "",
            "Részletek:",
            f"Meglévő weboldal: {quote.get_existing_site_display() or '-'}"
            + (f" ({quote.website_url})" if quote.website_url else ""),
            f"Domain: {quote.get_domain_display() or '-'}"
            + (f" ({quote.domain_name})" if quote.domain_name else ""),
            f"Méret: {quote.get_size_display() or '-'}",
            f"Nyelvek: {', '.join(quote.language_labels()) or '-'}",
            f"Kiegészítők: {', '.join(quote.addon_labels()) or '-'}",
            f"Határidő: {quote.get_timeline_display() or '-'}",
            f"Keretösszeg: {quote.get_budget_display() or '-'}",
            f"Sopron környéki: {'igen' if quote.is_local else 'nem'}",
            f"Pályázati forrásból: {'igen' if quote.is_grant_funded else 'nem'}",
        ]
    if quote.site_check:
        lines += ["", *_site_check_lines(quote.site_check)]
    return "\n".join(lines)


SCORE_LABELS = (
    ("performance", "Teljesítmény"),
    ("accessibility", "Akadálymentesség"),
    ("bestPractices", "Bevált gyakorlatok"),
    ("seo", "SEO"),
)
DEVICES = {"mobile": "mobil", "desktop": "asztali"}
# The SEO basics and technical details of an attached check (ids from the
# site checker), in Hungarian for the mail.
CHECK_LABELS = {
    "structuredData": "strukturált adatok",
    "title": "oldalcím",
    "description": "meta leírás",
    "h1": "H1 címsor",
    "indexable": "indexelhetőség",
    "canonical": "canonical",
    "viewport": "mobil nézet",
    "lang": "nyelv jelölése",
    "social": "megosztási adatok",
    "hreflang": "nyelvi változatok",
    "images": "képek alt szövege",
    "https": "HTTPS",
    "robots": "robots.txt",
    "sitemap": "sitemap",
    "pageWeight": "oldalméret",
    "fonts": "betűtípusok",
    "javascript": "JavaScript",
    "codeSplitting": "kódfelosztás",
    "css": "CSS",
    "cache": "gyorsítótárazás",
    "domSize": "DOM méret",
    "thirdParty": "külső szolgáltatások",
    "compression": "tömörítés",
    "imageFormats": "képformátumok",
}


def _site_check_lines(check):
    """The attached website check, readably; tolerant of missing fields."""
    scores = check.get("scores") or {}
    lines = [
        f"Csatolt weboldal-ellenőrzés ({DEVICES.get(check.get('strategy'), check.get('strategy', '-'))}):",
        f"Oldal: {check.get('finalUrl') or check.get('url', '-')}",
        "Pontszámok: "
        + ", ".join(f"{label} {scores.get(key, '-')}" for key, label in SCORE_LABELS),
    ]
    for metric in check.get("lab") or []:
        lines.append(f"  {metric.get('title', '')}: {metric.get('value', '')}")
    issues = [
        item
        for item in [*(check.get("seo") or []), *(check.get("tech") or [])]
        if item.get("status") in ("fail", "warn")
    ]
    if issues:
        lines.append(
            "SEO és technikai figyelmeztetések: "
            + ", ".join(
                f"{CHECK_LABELS.get(item.get('id'), item.get('id'))}"
                f"{' (hiba)' if item.get('status') == 'fail' else ''}"
                for item in issues
            )
        )
    wins = check.get("opportunities") or []
    if wins:
        lines.append("Legnagyobb javítási lehetőségek:")
        for item in wins:
            savings = item.get("savingsMs") or 0
            extra = f" (~{savings / 1000:.1f} s)" if savings >= 100 else ""
            if not extra and item.get("clsSavings"):
                extra = f" (CLS −{item['clsSavings']})"
            lines.append(f"  - {item.get('title', '')}{extra}")
    return lines


def _send(quote, recipient):
    try:
        EmailMessage(
            subject=f"Új ajánlatkérés: {quote.name} ({quote.service_name or quote.service})",
            body=_body(quote),
            to=[recipient],
            reply_to=[quote.email],
        ).send(fail_silently=False)
    except Exception:  # noqa: BLE001 - a mail outage must not lose the request
        logger.exception("Could not send the quote request notification (id=%s)", quote.pk)


def notify_new_quote(quote, *, run_async=True):
    recipient = getattr(settings, "QUOTE_NOTIFY_EMAIL", "")
    if not recipient or not getattr(settings, "EMAIL_HOST", ""):
        return False
    if run_async:
        threading.Thread(target=_send, args=(quote, recipient), daemon=True).start()
    else:
        _send(quote, recipient)
    return True
