"""Celery result view."""
import datetime

from django.conf import settings

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
        celery_result = self.get_object()
        logs_after = self.request.query_params.get("logs_after", None)
        if logs_after:
            logs_after_datetime = datetime.datetime.strptime(logs_after, "%Y-%m-%dT%H:%M:%S.%fZ")
            logs = celery_result.logs.filter(created__gt=logs_after_datetime)
        else:
            logs = celery_result.logs.all()
        serializer = self.get_serializer(celery_result, context={"logs": logs})
        return Response(serializer.data)
