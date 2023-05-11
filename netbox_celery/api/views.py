"""Celery result view."""
import datetime

from rest_framework.response import Response

from netbox_celery.api.serializers import CeleryResultSerializer
from netbox_celery.filtersets import CeleryResultFilterSet
from netbox_celery.models import CeleryResult, CeleryLogEntry

from netbox.api.viewsets import NetBoxModelViewSet


class CeleryResultView(NetBoxModelViewSet):
    """CeleryResult view."""

    queryset = CeleryResult.objects.all()
    filterset_class = CeleryResultFilterSet
    serializer_class = CeleryResultSerializer

    def retrieve(self, request, *args, **kwargs):
        job_result = kwargs.get("pk")
        celery_result = self.get_object()
        logs_after = self.request.query_params.get("logs_after")
        logs_after_datetime = None
        if logs_after:
            logs_after_datetime = datetime.datetime.strptime(logs_after, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                tzinfo=datetime.timezone.utc
            )
        if logs_after_datetime:
            logs = CeleryLogEntry.objects.filter(job_result=job_result, created__gt=logs_after_datetime)
        else:
            logs = CeleryLogEntry.objects.filter(job_result=job_result)
        serializer = self.get_serializer(celery_result, context={"logs": logs})
        return Response(serializer.data)
