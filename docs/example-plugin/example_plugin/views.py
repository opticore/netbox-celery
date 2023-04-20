"""Views for the example plugin."""
from django.contrib.auth.mixins import PermissionRequiredMixin

from netbox_celery.views import CeleryTaskAddView
from example_plugin.forms import ExampleTaskForm


class ExampleAddView(PermissionRequiredMixin, CeleryTaskAddView):
    """OnboardDevice add view."""

    permission_required = "example_plugin.add_example"
    form = ExampleTaskForm
