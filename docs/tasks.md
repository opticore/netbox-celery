# Celery Tasks

Tasks are the building blocks of Celery applications.

A task is a class that can be created out of any callable. It performs dual roles in that it defines both what happens when a task is called (sends a message), and what happens when a worker receives that message.

Every task class has a unique name, and this name is referenced in messages so the worker can find the right function to execute. The task will be referenced from the plugin name and the task name.

## Base Class `netbox_celery.tasks.CeleryBaseTask`

To ensure every task built in other projects has all the required features necessary for `netbox_celery` to work, a base class as been implemented for all Celery tasks.

### Building a Celery Task

The example below shows a very simple Celery task. Using the `shared_task` decorator with the three key word arguments creates a registered tasks which a worker can pick up.

Required key work arguments:

- `name` (str): Defines the name of the task. The plugin name should be used to stop any overlapping tasks.
- `base` (class): Set the base class to bind with.
- `bind` (bool): Binds the function with the base class.

When the task is bound to the base, it inherits functions for logging and reporting task status. It also overwrites the `run()` function in the base class with the code from your function.

Whenever `CeleryBaseTask` is used, the first argument in the celery function needs to be `task_id`. This allows the backend to retrieve the correct `CeleryResult` object from the ORM. Additional arguments can be added after `task_id` depending on the function.

``` python
# Example script
from celery import shared_task
from netbox_celery.tasks import CeleryBaseTask


@shared_task(name="netbox_example_plugin:hello_world", base=CeleryBaseTask, bind=True)
def hello_world(self, task_id):
    self.log("Hello World!")
```

``` bash
# Example output
celery -A netbox_celery worker -E -l INFO

 -------------- celery@opticore v5.2.7 (dawn-chorus)
--- ***** -----
-- ******* ---- macOS-13.0-arm64-arm-64bit 2023-03-29 12:03:47
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         netbox_celery:0x10a1adf10
- ** ---------- .> transport:   redis://localhost:6379//
- ** ---------- .> results:     redis://localhost:6379/0
- *** --- * --- .> concurrency: 10 (prefork)
-- ******* ---- .> task events: ON
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery


[tasks]
  . netbox_example_plugin:hello_world

[2023-03-29 12:03:50,308: INFO/MainProcess] celery@opticoreit ready.
[2023-03-29 12:06:52,237: INFO/MainProcess] Task netbox_example_plugin:hello_world[d3d71f5b-fd0a-4a9e-9043-c381f72b5899] received
[2023-03-29 12:07:04,367: INFO/ForkPoolWorker-8] Task netbox_example_plugin:hello_world[d3d71f5b-fd0a-4a9e-9043-c381f72b5899] succeeded in 12.120981917000023s: None
```
