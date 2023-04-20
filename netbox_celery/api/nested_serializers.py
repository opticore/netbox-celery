from netbox.api.serializers import NetBoxModelSerializer

from netbox_celery.models import CeleryLogEntry


class NestedCeleryLogEntrySerializer(NetBoxModelSerializer):
    """Nested CeleryLogEntry serializer."""

    class Meta:
        """Meta Class."""

        model = CeleryLogEntry
        fields = [
            "log_level",
            "grouping",
            "message",
            "created",
        ]
