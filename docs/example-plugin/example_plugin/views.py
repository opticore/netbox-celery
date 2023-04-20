"""Views for the example plugin."""
from netbox_celery.views import CeleryTaskAddView
from example_plugin.forms import ExampleTaskForm


class ExampleAddView(CeleryTaskAddView):
    """OnboardDevice add view."""

    form = ExampleTaskForm
