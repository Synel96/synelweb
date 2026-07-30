from django.db import models


class ExchangeRate(models.Model):
    """Cached HUF -> target currency conversion rate, refreshed daily."""

    BASE_CURRENCY = "HUF"

    target_currency = models.CharField(max_length=3, unique=True)
    rate = models.DecimalField(
        max_digits=12, decimal_places=6,
        help_text="1 HUF árfolyama a target_currency-ban",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["target_currency"]

    def __str__(self):
        return f"{self.BASE_CURRENCY} -> {self.target_currency}: {self.rate}"
