from rest_framework import generics
from core.models import Package
from .serializers import PackageSerializer


class PackageListAPIView(generics.ListAPIView):
    serializer_class = PackageSerializer

    def get_queryset(self):
        return Package.objects.all().order_by("id")
