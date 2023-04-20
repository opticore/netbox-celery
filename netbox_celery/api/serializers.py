"""Netbox Celery API serializers."""
from netbox.api.serializers import NetBoxModelSerializer

from netbox_celery.api.nested_serializers import NestedCeleryLogEntrySerializer
from netbox_celery.models import CeleryResult


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
            "logs",
        ]

    def to_representation(self, instance):
        logs = self.context.get('logs')
        logs_after = NestedCeleryLogEntrySerializer(
            logs,
            many=True,
            read_only=True
            ).data
        representation = super().to_representation(instance)
        representation['logs'] = logs_after
        return representation
