from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Package

from .currency import TARGET_CURRENCIES, get_rate
from .models import ExchangeRate
from .serializers import PackageSerializer


class PackageListAPIView(generics.ListAPIView):
    serializer_class = PackageSerializer

    def get_queryset(self):
        return Package.objects.all().order_by("id")


class ExchangeRateAPIView(APIView):
    """HUF -> EUR/USD rates, the same ones the services API converts with.

    Lets the frontend show other HUF amounts (budget bands, the maintenance
    fee) in the visitor's currency without hard-coding a rate.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        rates = {}
        for currency in TARGET_CURRENCIES:
            rate = get_rate(currency)
            if rate is not None:
                rates[currency] = float(rate)
        response = Response({"base": ExchangeRate.BASE_CURRENCY, "rates": rates})
        # Rates change daily at most; let browsers and the CDN reuse them.
        response["Cache-Control"] = "public, max-age=3600"
        return response
