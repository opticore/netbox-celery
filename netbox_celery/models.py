"""Netbox Celery Models."""
import logging
import uuid

from celery import current_app
from celery.exceptions import NotRegistered
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.urls import reverse
from django.utils import timezone
from netbox_celery.choices import CeleryResultStatusChoices, LogLevelIntegerChoices
from users.models import User
from utilities.querysets import RestrictedQuerySet

from netbox.models import NetBoxModel

logger = logging.getLogger("netbox_celery.models")


class CeleryResult(NetBoxModel):
    """Celery Result Class.

    This class is used to store the results of celery tasks.

    Attributes:
        task_id (UUIDField): The UUID of the task.
        celery_name (CharField): The name of the celery task.
        created (DateTimeField): The date and time the task was created.
        completed (DateTimeField): The date and time the task was completed.
        user (ForeignKey): The user that created the task.
        status (CharField): The status of the task.
        args (JSONField): The args of the task.
        kwargs (JSONField): The kwargs of the task.
        job_kwargs (JSONField): The job_kwargs of the task.
        result (JSONField): The result of the task.
    """

    task_id = models.UUIDField(unique=True)
    celery_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="+", blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices=CeleryResultStatusChoices,
        default=CeleryResultStatusChoices.STATUS_PENDING,
    )
    args = models.JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)
    kwargs = models.JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)
    job_kwargs = models.JSONField(blank=True, null=True, encoder=DjangoJSONEncoder)
    result = models.JSONField(blank=True, null=True, encoder=DjangoJSONEncoder)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        """Meta Class."""

        verbose_name = "Celery Result"
        verbose_name_plural = "Celery Results"
        ordering = ["-created"]

    def __str__(self):
        """String representation."""
        return f"{self.celery_name} - {self.status}"

    def get_absolute_url(self):
        """Get absolute url."""
        return reverse("plugins:netbox_celery:celeryresult_view", kwargs={"pk": self.pk})

    @classmethod
    def enqueue_job(  # pylint: disable=dangerous-default-value
        cls,
        celery_name,
        user,
        celery_kwargs={},
        task_id=None,
        args=[],
        kwargs={},
    ):
        """Enqueue job."""

        if not task_id:
            task_id = uuid.uuid4()

        celery_result = cls.objects.create(
            celery_name=celery_name,
            user=user,
            task_id=task_id,
            args=args,
            kwargs=kwargs,
        )

        # Prepare args that will be sent to Celery with the CeleryResult pk
        args = [celery_result.pk] + list(args)

        try:
            current_app.loader.import_default_modules()
            func = current_app.tasks[celery_name]
            func.apply_async(
                args=args,
                kwargs=kwargs,
                task_id=str(celery_result.task_id),
                **celery_kwargs,
            )
        except NotRegistered:
            logger.error("Task %s not registered", celery_name)
            celery_result.result(f"Task {celery_name} not registered")
            celery_result.status = CeleryResultStatusChoices.STATUS_FAILED
            celery_result.save()
        return celery_result

    def log(self, level_choice, message, grouping="main"):
        """Log message."""
        CeleryLogEntry.objects.create(
            job_result=self,
            log_level=level_choice,
            grouping=grouping,
            message=message,
            created=timezone.now().isoformat(),
        )

    def log_debug(self, message, grouping="main"):
        """Log info message."""
        self.log(LogLevelIntegerChoices.LOG_DEBUG, message, grouping)

    def log_info(self, message, grouping="main"):
        """Log info message."""
        self.log(LogLevelIntegerChoices.LOG_INFO, message, grouping)

    def log_success(self, message, grouping="main"):
        """Log success message."""
        self.log(LogLevelIntegerChoices.LOG_SUCCESS, message, grouping)

    def log_warning(self, message, grouping="main"):
        """Log warning message."""
        self.log(LogLevelIntegerChoices.LOG_WARNING, message, grouping)

    def log_failure(self, message, grouping="main"):
        """Log failure message."""
        self.log(LogLevelIntegerChoices.LOG_FAILURE, message, grouping)


class CeleryLogEntry(models.Model):
    """Stores each log entry for the CeleryResult."""

    job_result = models.ForeignKey(CeleryResult, on_delete=models.CASCADE, related_name="logs")
    log_level = models.CharField(
        max_length=32,
        choices=LogLevelIntegerChoices,
        default=LogLevelIntegerChoices.LOG_DEFAULT,
        db_index=True,
    )
    grouping = models.CharField(max_length=100, default="main")
    message = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.message)

    class Meta:
        """Meta Class."""

        ordering = ["created"]
        get_latest_by = "created"
        verbose_name_plural = "Celery Log Entries"
