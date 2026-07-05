from rest_framework import generics
from core.models import Project
from .serializers import ProjectSerializer


class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all().order_by("id")