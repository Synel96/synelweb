from rest_framework import generics
from core.models import Package
from .serializers import PackageSerializer

class PackageListAPIView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
