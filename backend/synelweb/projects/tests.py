import json

from django.test import SimpleTestCase

from core.models import Project

from .serializers import ProjectSerializer


class ProjectOrderTests(SimpleTestCase):
    """The order the frontend sorts projects by (ascending)."""

    def order_of(self, project):
        return ProjectSerializer().get_order(project)

    def test_newest_project_comes_first_without_an_explicit_order(self):
        older = Project(id=3, name="Régebbi", project_type="Weboldal", description="")
        newer = Project(id=7, name="Legújabb", project_type="Webshop", description="")

        self.assertLess(self.order_of(newer), self.order_of(older))

    def test_explicitly_ordered_projects_come_before_the_rest(self):
        pinned = Project(
            id=1, name="Kiemelt", project_type="Webshop", description=json.dumps({"order": 5})
        )
        newest = Project(id=99, name="Legújabb", project_type="Webshop", description="")

        self.assertLess(self.order_of(pinned), self.order_of(newest))

    def test_own_project_flag(self):
        own = Project(id=1, name="SynelWeb", project_type="Weboldal", description=json.dumps({"ownProject": True}))
        client = Project(id=2, name="AlphaDent", project_type="Weboldal", description="")

        self.assertTrue(ProjectSerializer().get_isOwnProject(own))
        self.assertFalse(ProjectSerializer().get_isOwnProject(client))

    def test_an_explicit_order_is_kept(self):
        project = Project(
            id=7, name="Kiemelt", project_type="Webshop", description=json.dumps({"order": 1})
        )

        self.assertEqual(self.order_of(project), 1)
