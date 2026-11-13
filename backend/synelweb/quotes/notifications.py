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
    return "\n".join(lines)


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
