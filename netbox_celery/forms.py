"""Forms for the netbox_celery plugin."""
import csv

from celery import current_app
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from users.models import User
from utilities.forms import (
    APISelectMultiple,
    BootstrapMixin,
    DateTimePicker,
    DynamicModelMultipleChoiceField,
    MultipleChoiceField,
)

from netbox.forms import NetBoxModelFilterSetForm
from netbox_celery.choices import CeleryResultStatusChoices
from netbox_celery.models import CeleryResult


class CeleryTaskForm(forms.Form):
    """Base form for Celery tasks."""

    class Meta:
        """Meta class for CeleryTaskForm."""

        fields = ()
        task_name = None

    def save(self, request):
        """Save the form."""
        return CeleryResult.enqueue_job(
            self.task_name,
            user=request.user,
            kwargs=self.cleaned_data,
        )


class CeleryTaskBulkForm(forms.Form):
    """Base form for bulk Celery tasks."""

    csv_file = forms.FileField(
        label="CSV File",
        help_text="CSV file containing the data for the task",
        required=False,
    )
    csv_data = forms.CharField(
        label="CSV Data",
        widget=forms.Textarea(attrs={"rows": "20"}),
        help_text="CSV data containing the data for the task",
        required=False,
    )

    class Meta:
        """Meta class for CeleryTaskBulkForm."""

        base_form = CeleryTaskForm
        task_name = None
        multi_celery_job = False

    def clean(self):
        if not (self.cleaned_data["csv_file"] or self.cleaned_data["csv_data"]):
            raise ValidationError("Please provide a CSV file or CSV data.")
        return self.cleaned_data

    def read_csv(self):
        """Read the CSV file or data."""
        if self.cleaned_data["csv_file"]:
            reader = csv.DictReader(self.cleaned_data["csv_file"])
        else:
            reader = csv.DictReader(self.cleaned_data["csv_data"].splitlines())
        return list(reader)

    def is_valid(self):
        """Check if the form is valid."""
        super().is_valid()
        csv_data = self.read_csv()
        for row in csv_data:
            form = self.Meta.base_form(row)
            if not form.is_valid():
                return False
        return True

    def data_to_kwargs(self, data):
        """Convert the data to kwargs."""
        raise NotImplementedError

    def save(self, request):
        """Save the form."""
        if not getattr(self.Meta, "task_name", None):
            raise ValidationError("Please provide a task name in Meta class.")

        csv_data = self.read_csv()

        if getattr(self.Meta, "multi_celery_job", None):
            jobs = []
            for data in csv_data:
                jobs.append(
                    CeleryResult.enqueue_job(
                        self.Meta.task_name,
                        user=request.user,
                        kwargs=self.data_to_kwargs(data),
                    )
                )
            return jobs
        return CeleryResult.enqueue_job(
            self.Meta.task_name,
            user=request.user,
            kwargs=self.data_to_kwargs(csv_data),
        )


class CeleryResultFilterSetForm(NetBoxModelFilterSetForm):
    """Celery result filterset form."""

    model = CeleryResult

    celery_name = forms.CharField()  # Added for ordering
    created__gte = forms.DateTimeField(
        label=_("Created (min)"),
        required=False,
        widget=DateTimePicker(),
    )
    created__lte = forms.DateTimeField(
        label=_("Created (max)"),
        required=False,
        widget=DateTimePicker(),
    )
    completed__gte = forms.DateTimeField(
        label=_("Completed (min)"),
        required=False,
        widget=DateTimePicker(),
    )
    completed__lte = forms.DateTimeField(
        label=_("Completed (max)"),
        required=False,
        widget=DateTimePicker(),
    )
    user_id = DynamicModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_("User"),
        widget=APISelectMultiple(
            api_url="/api/users/users/",
        ),
    )
    status = MultipleChoiceField(choices=CeleryResultStatusChoices, required=False)

    def __init__(self, *args, **kwargs):
        """Custom celery job name field."""
        super().__init__(*args, **kwargs)
        current_app.loader.import_default_modules()
        tasks = []
        for task in current_app.tasks.keys():
            if task.startswith("celery."):
                continue
            tasks.append((task, task))
        self.fields["celery_name"] = MultipleChoiceField(
            choices=tasks,
            required=False,
            label=_("Celery Name"),
        )
