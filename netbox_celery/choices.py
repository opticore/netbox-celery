"""Netbox Celery choices."""
from utilities.choices import ChoiceSet


class CeleryResultStatusChoices(ChoiceSet):
    """Job result status choices."""

    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_COMPLETED = "completed"
    STATUS_ERRORED = "errored"
    STATUS_FAILED = "failed"

    CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_RUNNING, "Running"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_ERRORED, "Errored"),
        (STATUS_FAILED, "Failed"),
    )

    TERMINAL_STATE_CHOICES = (
        STATUS_COMPLETED,
        STATUS_ERRORED,
        STATUS_FAILED,
    )


class LogLevelChoices(ChoiceSet):
    """Log level choices."""

    LOG_DEFAULT = "default"
    LOG_SUCCESS = "success"
    LOG_INFO = "info"
    LOG_WARNING = "warning"
    LOG_FAILURE = "failure"

    CHOICES = (
        (LOG_DEFAULT, "Default", "gray"),
        (LOG_SUCCESS, "Success", "green"),
        (LOG_INFO, "Info", "cyan"),
        (LOG_WARNING, "Warning", "yellow"),
        (LOG_FAILURE, "Failure", "red"),
    )


class LogLevelIntegerChoices(ChoiceSet):
    """Log level choices."""

    LOG_DEFAULT = 20
    LOG_DEBUG = 10
    LOG_INFO = 20
    LOG_SUCCESS = 25
    LOG_WARNING = 30
    LOG_FAILURE = 40
    LOG_ERROR = 40
    LOG_CRITICAL = 50

    CHOICES = (
        (LOG_DEFAULT, "Default"),
        (LOG_DEBUG, "Debug"),
        (LOG_INFO, "Info"),
        (LOG_SUCCESS, "Success"),
        (LOG_WARNING, "Warning"),
        (LOG_FAILURE, "Failure"),
        (LOG_ERROR, "Error"),
        (LOG_CRITICAL, "Critical"),
    )
