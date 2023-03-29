# CeleryResult

## Attributes

- task_id (UUIDField): The UUID of the task.
- celery_name (CharField): The name of the celery task.
- created (DateTimeField): The date and time the task was created.
- completed (DateTimeField): The date and time the task was completed.
- user (ForeignKey): The user that created the task.
- status (CharField): The status of the task.
- args (JSONField): The args of the task.
- kwargs (JSONField): The kwargs of the task.
- job_kwargs (JSONField): The job_kwargs of the task.
- result (JSONField): The result of the task.

## `enqueue_job()` method

This method of the model runs the task against Celery. When using this model to create a task, this is the only function that should be ran.

Example:

``` python
from netbox_celery.models import CeleryResult

job = CeleryResult.enqueue_job(
    "example_plugin:example_job",       # Name/Path of celery function
    user=None,                          # User who initiated the job
    celery_kwargs={"countdown": 10},    # kwargs that are passed into `apply_async`
    args=[],                            # args that are passed into celery task function
    kwargs=[],                          # kwargs that are passed into celery task function
)
```

Above shows how to initiate a celery job using the model. This will create a new entry in the model and add the job to the celery que. This will then be picked up by an available worker.
