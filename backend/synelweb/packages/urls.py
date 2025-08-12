from django.urls import path
from .views import PackageListAPIView

urlpatterns = [
    path("list/",PackageListAPIView.as_view(), name="package-list"),
]