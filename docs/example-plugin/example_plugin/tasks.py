"""Example Tasks File."""
from netbox_celery.tasks import netbox_celery_task
import time

@netbox_celery_task(name="example_plugin:hello_world")
def hello_world(self, task_id, name="World"):  # pylint: disable=unused-argument
    """Example hello world task."""
    time.sleep(7)
    self.log(f"Hello {name}!")
