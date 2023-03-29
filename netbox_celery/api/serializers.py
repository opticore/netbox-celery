"""Netbox Celery API serializers."""
from netbox_celery.models import CeleryResult

from netbox.api.serializers import NetBoxModelSerializer


class CeleryResultSerializer(NetBoxModelSerializer):
    """CeleryResult serializer."""

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
        ]
