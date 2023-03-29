"""Netbox Celery Plugin."""
from extras.plugins import PluginConfig
from .celery import app as celery_app  # noqa


__version__ = "0.1.0"


class NetboxCeleryConfig(PluginConfig):
    """Plugin configuration for netbox_awx_runner."""

    name = "netbox_celery"
    verbose_name = "Netbox Celery"
    version = __version__
    author = "OpticoreIT"
    author_email = "info@opticoreit.com"
    description = "Celery job management for Netbox."
    base_url = "celery"

    django_apps = [
        "django_celery_beat",
    ]


config = NetboxCeleryConfig  # pylint: disable=invalid-name
