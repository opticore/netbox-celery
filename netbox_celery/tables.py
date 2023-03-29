"""Netbox Celery Tables."""
import django_tables2 as tables
from netbox_celery.models import CeleryResult

from netbox.tables import NetBoxTable, columns


class CeleryResultTable(NetBoxTable):
    """Celery result table."""

    task_id = tables.Column(linkify=True, verbose_name="Task ID")
    actions = columns.ActionsColumn(
        actions=("delete",),
    )

    class Meta(NetBoxTable.Meta):
        """Meta."""

        name = "celery_results"
        model = CeleryResult
        fields = (
            "task_id",
            "celery_name",
            "created",
            "completed",
            "user",
            "status",
        )
        attrs = {"class": "table table-hover table-headings"}
        datatable_ordering = [[3, "desc"]]
