"""Test cases for the CeleryResult views."""
import uuid
from netbox_celery.models import CeleryResult

from utilities.testing import ViewTestCases, create_tags


class CeleryResultTestCase(
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    """Test cases for the CeleryResult views."""

    model = CeleryResult

    def _get_base_url(self):
        """Return the base URL for the view."""
        return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        CeleryResult.objects.bulk_create(
            [
                CeleryResult(task_id=uuid.uuid4(), status="SUCCESS"),
                CeleryResult(task_id=uuid.uuid4(), status="SUCCESS"),
                CeleryResult(task_id=uuid.uuid4(), status="SUCCESS"),
            ]
        )

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "task_id": uuid.uuid4(),
            "status": "SUCCESS",
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "task_id,status",
            f"{uuid.uuid4()},SUCCESS",
            f"{uuid.uuid4()},SUCCESS",
            f"{uuid.uuid4()},SUCCESS",
        )

        cls.bulk_edit_data = {
            "status": "SUCCESS",
        }
