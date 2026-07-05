from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from core.models import Review
from .serializers import ReviewSerializer


class ReviewCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Public endpoint: only approved reviews are visible.
        return Review.objects.filter(is_approved=True).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            {
                "id": str(instance.id),
                "status": "pending_approval",
            },
            status=status.HTTP_201_CREATED,
        )
