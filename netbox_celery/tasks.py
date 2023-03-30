"""Base tasks for Celery."""
import logging

from datetime import datetime
from celery.app.task import Task
from celery import shared_task

from netbox_celery.choices import CeleryResultStatusChoices
from netbox_celery.models import CeleryResult

logger = logging.getLogger("netbox_celery.tasks")


class CeleryBaseTask(Task):
    """Celery Base Task."""

    name = ""
    description = ""
    ignore_result = False
    validation_class = ""
    task_id = None
    task_obj = None

    def __call__(self, task_id, *args, **kwargs):
        """Call task."""
        self.task_id = task_id
        self.get_result_obj(task_id)
        self.task_obj.status = CeleryResultStatusChoices.STATUS_RUNNING
        self.task_obj.save()
        return super().__call__(task_id, *args, **kwargs)

    def run(self, task_id):  # pylint: disable=arguments-differ
        """Run task."""
        raise NotImplementedError("You must implement the run method.")

    def on_success(self, retval, task_id, args, kwargs):
        """On success."""
        if self.task_obj.status not in [
            CeleryResultStatusChoices.STATUS_FAILED,
            CeleryResultStatusChoices.STATUS_ERRORED,
        ]:
            self.task_obj.status = CeleryResultStatusChoices.STATUS_COMPLETED
        self.task_obj.completed = datetime.now()
        self.task_obj.save()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """On failure."""
        if self.task_obj:
            self.task_obj.status = CeleryResultStatusChoices.STATUS_FAILED
            self.task_obj.completed = datetime.now()
            for line in einfo.traceback.splitlines():
                self.log(logging.ERROR, str(line))
            self.task_obj.save()

    def get_result_obj(self, primary_key):
        """Get result object."""
        self.task_obj = CeleryResult.objects.get(pk=primary_key)
        return self.task_obj

    def log(self, level_choice=logging.INFO, message=""):
        """Log message."""
        self.task_obj.log(level_choice, message)


def netbox_celery_task(*args, base=CeleryBaseTask, bind=True, **kwargs):
    """Netbox Celery Task Decorator.

    This decorator is used to set default values for the Celery task.

    Args:
        base (CeleryBaseTask): Base task class.
        bind (bool): Bind task to instance.

    """

    def _netbox_celery_task(*args, **kwargs):
        return shared_task(*args, **kwargs)

    return _netbox_celery_task(*args, base=base, bind=bind, **kwargs)
