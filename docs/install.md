# Installation

## Package and Plugin Configuration

1. Install the package using pip:

    ``` bash
    pip install netbox-celery
    ```

2. Add plugin to `PLUGINS` in configuration:

    ``` python
    PLUGINS = [
        ...
        "netbox_celery",
        ...
    ]
    ```

## Additional Processes

To be able to run jobs, three process will need to be started:

- Redis Server
- Celery Worker
- Celery Beat (optional)

### Local

The following steps are for local development. For any server deployments please use docker.

#### Redis Server

For netbox to work, mostly you will already have redis-server installed.

1. Install `redis-server` to the linux machine (https://redis.io/docs/getting-started/):

    ``` bash
    # Debian
    $ sudo apt-get install redis

    # Redhat/Centos
    $ sudo yum install redis

    # Mac
    $ brew install redis-server
    ```

2. Start `redis-server` service.

3. Test installation:

    ``` bash
    $ redis-cli ping
    PONG
    ```

#### Celery Worker

1. Enable virtual environment if using one.
2. Change directory to netbox folder where `manage.py` is located.
3. Start worker. Options (The order is important):

    - A:     Defines the app Celery needs to use. This should always be `netbox_celery` plugin.
    - arg:    Entry point for celery
    - l:     Log level for celery

    ``` bash
    celery -A netbox_celery worker -l INFO
    ```

The output should display all available tasks inside of your netbox instance.

``` bash
❯ celery -A netbox_celery worker -l INFO

 -------------- celery@Kristians-MacBook-Pro.local v5.2.7 (dawn-chorus)
--- ***** ----- 
-- ******* ---- macOS-13.0-arm64-arm-64bit 2023-03-23 12:16:58
- *** --- * --- 
- ** ---------- [config]
- ** ---------- .> app:         netbox_celery:0x105ca71c0
- ** ---------- .> transport:   redis://localhost:6379//
- ** ---------- .> results:     redis://localhost:6379/0
- *** --- * --- .> concurrency: 10 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . netbox_config_backup:backup_device
  . netbox_config_backup:backup_email_report
  . netbox_device_onboarder:device_onboard

[2023-03-23 12:17:00,105: INFO/MainProcess] Connected to redis://localhost:6379//
[2023-03-23 12:17:00,108: INFO/MainProcess] mingle: searching for neighbors
[2023-03-23 12:17:01,141: INFO/MainProcess] mingle: all alone
```

#### Celery Beat

1. Enable virtual environment if using one.
2. Change directory to netbox folder where `manage.py` is located.
3. Start worker. Options (The order is important):

    - A: Defines the app Celery needs to use. This should always be `netbox_celery` plugin.
    - arg: Entry point for celery
    - l: Log level for celery
    - S: Defines custom scheduling class necessary to work with `CeleryResult` model.

    ``` bash
    celery -A netbox_celery beat -l INFO -S netbox_celery.schedule.NetboxCeleryDatabaseScheduler
    ```

The output should display all available tasks inside of your netbox instance.

``` bash
celery beat v5.2.7 (dawn-chorus) is starting.
__    -    ... __   -        _
LocalTime -> 2023-03-23 12:21:56
Configuration ->
    . broker -> redis://localhost:6379//
    . loader -> celery.loaders.app.AppLoader
    . scheduler -> netbox_celery.schedule.NetboxCeleryDatabaseScheduler

    . logfile -> [stderr]@%INFO
    . maxinterval -> 5.00 seconds (5s)
[2023-03-23 12:21:56,254: INFO/MainProcess] beat: Starting...
```
