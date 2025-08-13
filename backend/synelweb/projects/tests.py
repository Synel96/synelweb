from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Project

class ProjectListAPITest(APITestCase):
    def setUp(self):
        Project.objects.create(
            name="Teszt Projekt",
            slug="teszt-projekt",
            project_type="Webshop",
            preview_video_url="https://youtube.com/testvideo",
            preview_image_url="https://pelda.hu/kep.png",
        )

    def test_project_list_api_returns_projects(self):
        url = reverse("project-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Teszt Projekt")