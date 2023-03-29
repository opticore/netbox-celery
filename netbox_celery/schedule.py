"""Celery beat scheduler for NetBox."""
import sys
from celery.beat import (
    SchedulingError,
    _evaluate_entry_args,
    _evaluate_entry_kwargs,
)
from celery.exceptions import reraise
from django_celery_beat.schedulers import DatabaseScheduler

from netbox_celery.models import CeleryResult


class NetboxCeleryDatabaseScheduler(DatabaseScheduler):
    """Custom Celery beat scheduler for NetBox."""

    def apply_async(self, entry, producer=None, advance=True, **kwargs):
        """Apply async."""
        # Update time-stamps and run counts before we actually execute,
        # so we have that done if an exception is raised (doesn't schedule
        # forever.)
        entry = self.reserve(entry) if advance else entry
        task = self.app.tasks.get(entry.task)

        try:
            entry_args = _evaluate_entry_args(entry.args)
            entry_kwargs = _evaluate_entry_kwargs(entry.kwargs)
            if task:
                return CeleryResult.enqueue_job(
                    entry.task,
                    user=None,
                    args=entry_args,
                    kwargs=entry_kwargs,
                )
            return self.send_task(entry.task, entry_args, entry_kwargs, producer=producer, **entry.options)
        except Exception as exc:  # pylint: disable=broad-except
            return reraise(
                SchedulingError,
                SchedulingError(f"Couldn't apply scheduled task {entry.name}: {exc}"),
                sys.exc_info()[2],
            )
        finally:
            self._tasks_since_sync += 1
            if self.should_sync():
                self._do_sync()
