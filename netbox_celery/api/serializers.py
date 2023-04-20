"""Netbox Celery API serializers."""
from rest_framework import serializers
from netbox_celery.models import CeleryResult, CeleryLogEntry

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


class ResultLogSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="job_result.user.username")
    status = serializers.ReadOnlyField(source="job_result.status")
    result_created = serializers.ReadOnlyField(source="job_result.created")
    result_completed = serializers.ReadOnlyField(source="job_result.completed")

    class Meta:
        model = CeleryLogEntry
        fields = [
            "username",
            "status",
            "result_created",
            "result_completed",
            "job_result",
            "log_level",
            "grouping",
            "message",
            "created",
        ]

    def get_queryset(self):
        return super().get_queryset().select_related("job_result__user")
