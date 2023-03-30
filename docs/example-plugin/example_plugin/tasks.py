"""Example Tasks File."""
from netbox_celery.tasks import netbox_celery_task


@netbox_celery_task(name="example_plugin:hello_world")
def hello_world(self, task_id):  # pylint: disable=unused-argument
    """Example hello world task."""
    self.log("Hello World!")
