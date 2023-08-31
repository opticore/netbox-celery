"""Test the NetBox Celery API."""
import uuid

from django.contrib.auth.models import User
from django.urls import reverse
from utilities.testing import APITestCase, APIViewTestCases

from netbox_celery.models import CeleryResult


class AppTest(APITestCase):
    def test_root(self):
        url = reverse("plugins-api:netbox_celery-api:api-root")
        response = self.client.get("{}?format=api".format(url), **self.header)
        self.assertEqual(response.status_code, 200)


class CeleryResultTest(
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
):
    """Test the CeleryResult API views."""

    model = CeleryResult
    brief_fields = sorted(
        [
            "task_id",
            "celery_name",
            "created",
            "completed",
            "status",
            "user",
            "args",
            "kwargs",
            "job_kwargs",
            "result",
            "logs",
        ]
    )
    bulk_update_data = {
        "status": "SUCCESS",
    }

    def _get_detail_url(self, instance):
        """Return the URL for the detail view of the given instance."""
        viewname = f"plugins-api:{self._get_view_namespace()}:{instance._meta.model_name}-detail"
        return reverse(viewname, kwargs={"pk": instance.pk})

    def _get_list_url(self):
        """Return the URL for the list view."""
        viewname = f"plugins-api:{self._get_view_namespace()}:{self.model._meta.model_name}-list"
        return reverse(viewname)

    @classmethod
    def setUpTestData(cls):
        """Create test data."""

        cls.celeryuser = User.objects.create_user(username='celeryuser', password='testpass')

        CeleryResult.objects.bulk_create(
            [
                CeleryResult(
                    task_id=uuid.uuid4(),
                    status="SUCCESS",
                    user=cls.celeryuser,
                ),
                CeleryResult(
                    task_id=uuid.uuid4(),
                    status="SUCCESS",
                    user=cls.celeryuser,
                ),
                CeleryResult(
                    task_id=uuid.uuid4(),
                    status="SUCCESS",
                    user=cls.celeryuser,
                ),
            ]
        )
