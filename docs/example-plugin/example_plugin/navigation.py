"""Navigation menu items for netbox_device_onboarder."""
from extras.plugins import PluginMenuItem


menu_items = (
    PluginMenuItem(
        link="plugins:example_plugin:example_add",
        link_text="Example Task",
        permissions=["example_plugin.example"],
    ),
)
