"""Netbox Celery Forms."""
from django import forms

from utilities.forms import BootstrapMixin

from netbox_celery.forms import CeleryTaskForm


class ExampleTaskForm(BootstrapMixin, CeleryTaskForm):
    """Form for the ExampleTask."""

    name = forms.CharField(
        label="Name",
        required=True,
    )

    class Meta:
        """Meta class for ExampleTaskForm."""

        fields = ("name",)
        task_name = "example_plugin:hello_world"
