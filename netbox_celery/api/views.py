"""API views for the netbox_celery plugin."""
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from netbox_celery.api.serializers import CeleryResultSerializer
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
