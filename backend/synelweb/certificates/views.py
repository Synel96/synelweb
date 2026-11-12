from rest_framework import generics

from .models import Certificate
from .serializers import CertificateSerializer


class CertificateListAPIView(generics.ListAPIView):
    serializer_class = CertificateSerializer
    authentication_classes = []
    permission_classes = []
    pagination_class = None

    def get_queryset(self):
        return Certificate.objects.filter(is_active=True)
