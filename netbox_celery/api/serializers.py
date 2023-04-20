"""Netbox Celery API serializers."""
from netbox.api.serializers import NetBoxModelSerializer

from netbox_celery.api.nested_serializers import NestedCeleryLogEntrySerializer
from netbox_celery.models import CeleryResult


class CeleryResultSerializer(NetBoxModelSerializer):
    """CeleryResult serializer."""

    logs = NestedCeleryLogEntrySerializer(many=True, read_only=True)

    class Meta:
        """Meta Class."""

        model = CeleryResult
        fields = [
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
