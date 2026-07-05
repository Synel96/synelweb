from rest_framework import generics
from core.models import Project
from .serializers import ProjectSerializer


class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.prefetch_related("extra_images").order_by("id")