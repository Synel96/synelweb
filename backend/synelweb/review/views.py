from rest_framework import generics
from core.models import Review
from .serializers import ReviewSerializer

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
