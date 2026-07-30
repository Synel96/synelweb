import logging
from decimal import Decimal, ROUND_HALF_UP

import requests
from django.utils import timezone

from .models import ExchangeRate

logger = logging.getLogger(__name__)

FRANKFURTER_URL = "https://api.frankfurter.app/latest"
TARGET_CURRENCIES = ["USD", "EUR"]
LANG_TO_CURRENCY = {"hu": "HUF", "en": "USD", "de": "EUR"}
STALE_AFTER = timezone.timedelta(hours=24)


def currency_for_lang(accept_language):
    lang = (accept_language or "").split(",")[0].split("-")[0].strip().lower()
    return LANG_TO_CURRENCY.get(lang, ExchangeRate.BASE_CURRENCY)


def fetch_rates():
    """Fetch HUF -> USD/EUR rates from frankfurter.app (ECB data) and upsert them."""
    response = requests.get(
        FRANKFURTER_URL,
        params={"from": ExchangeRate.BASE_CURRENCY, "to": ",".join(TARGET_CURRENCIES)},
        timeout=10,
    )
    response.raise_for_status()
    rates = response.json().get("rates", {})
    for currency, rate in rates.items():
        ExchangeRate.objects.update_or_create(
            target_currency=currency,
            defaults={"rate": Decimal(str(rate))},
        )
    return rates


def _get_cached_rate(currency):
    entry = ExchangeRate.objects.filter(target_currency=currency).first()
    is_stale = entry is None or timezone.now() - entry.updated_at > STALE_AFTER
    if is_stale:
        try:
            fetch_rates()
            entry = ExchangeRate.objects.filter(target_currency=currency).first()
        except requests.RequestException:
            logger.warning("Failed to refresh exchange rates from frankfurter.app", exc_info=True)
    return entry.rate if entry else None


def convert_from_huf(amount_huf, currency):
    """Convert a HUF amount to the given currency, returning None if no rate is available."""
    if amount_huf is None:
        return None
    if currency == ExchangeRate.BASE_CURRENCY:
        return Decimal(amount_huf).quantize(Decimal("0.01"))

    rate = _get_cached_rate(currency)
    if rate is None:
        return None

    return (Decimal(amount_huf) * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
