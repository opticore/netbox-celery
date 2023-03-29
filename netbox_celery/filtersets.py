"""Celery result filtersets."""
import django_filters
from django.utils.translation import gettext as _
from netbox_celery.models import CeleryResult
from users.models import User


class CeleryResultFilterSet(django_filters.FilterSet):
    """Filter for celery results."""

    user = django_filters.ModelMultipleChoiceFilter(
        field_name="user__username",
        queryset=User.objects.all(),
        label=_("User"),
    )

    class Meta:
        """Meta."""

        model = CeleryResult
        fields = [
            "task_id",
            "celery_name",
            "created",
            "completed",
            "status",
            "user",
        ]
