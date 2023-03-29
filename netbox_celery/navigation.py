"""Navigation menu items for netbox_celery."""
from extras.plugins import PluginMenuItem


menu_items = (
    PluginMenuItem(
        link="plugins:netbox_celery:celeryresult_list",
        link_text="Celery Results",
        permissions=["netbox_celery.view_celeryresult"],
    ),
)
