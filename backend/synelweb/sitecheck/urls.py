from django.urls import path

from .views import SiteCheckAPIView

urlpatterns = [
    path("", SiteCheckAPIView.as_view(), name="site-check"),
]
