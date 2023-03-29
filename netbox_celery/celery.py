"""Celery configuration."""
import os

from celery import Celery
from django.conf import settings

from netbox_celery.settings_funcs import parse_redis_connection


# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netbox.settings")

# Get the base REDIS URL, default to redis' default
BASE_REDIS_URL = parse_redis_connection(redis_database=0)
app = Celery(
    "netbox_celery",
    backend=parse_redis_connection(redis_database=0),
)

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=False)

app.conf.broker_url = BASE_REDIS_URL

# this allows you to schedule items in the Django admin.
app.conf.beat_scheduler = "django_celery_beat.schedulers.DatabaseScheduler"
