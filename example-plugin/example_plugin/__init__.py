"""Netbox Celery Plugin."""
from extras.plugins import PluginConfig


__version__ = "0.0.1"


class ExamplePlugin(PluginConfig):
    """Example Plugin."""

    name = "example_plugin"
    verbose_name = "Example Plugin"
    version = __version__
    author = "OpticoreIT"
    author_email = "info@opticoreit.com"
    description = "Celery job management for Netbox."
    base_url = "celery"


config = ExamplePlugin  # pylint: disable=invalid-name
