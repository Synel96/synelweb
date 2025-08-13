from rest_framework import generics
from core.models import Project
from .serializers import ProjectSerializer

class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer