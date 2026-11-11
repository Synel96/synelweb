from django.urls import path

from .views import QuoteRequestCreateAPIView

urlpatterns = [
    path("", QuoteRequestCreateAPIView.as_view(), name="quote-request-create"),
]
