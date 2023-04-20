"""API views for the netbox_celery plugin."""
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from netbox_celery.api.serializers import (
    CeleryResultSerializer,
    ResultLogSerializer
)
from netbox_celery.filtersets import CeleryResultFilterSet
from netbox_celery.models import CeleryResult, CeleryLogEntry

from netbox.api.viewsets import NetBoxModelViewSet

#
# Celery Results
#


class CeleryResultView(NetBoxModelViewSet):
    """CeleryResult view."""

    queryset = CeleryResult.objects.all()
    filterset_class = CeleryResultFilterSet
    serializer_class = CeleryResultSerializer


class ResultLogViewSet(ReadOnlyModelViewSet):
    """ResultLog ViewSet."""
    queryset = CeleryLogEntry.objects.all()
    serializer_class = ResultLogSerializer

    def retrieve(self, request, *args, **kwargs):
        job_result = kwargs['pk']
        latest = self.request.query_params.get("latest")
        if latest:
            log = CeleryLogEntry.objects.filter(
                job_result=job_result,
                created__gt=latest
                )
        else:
            log = CeleryLogEntry.objects.filter(job_result=job_result)
        serializer = self.get_serializer(log, many=True)
        return Response(serializer.data)
