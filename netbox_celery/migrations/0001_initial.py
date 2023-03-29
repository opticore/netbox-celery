# Generated by Django 4.1.5 on 2023-01-31 15:01

from django.conf import settings
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("extras", "0077_customlink_extend_text_and_url"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CeleryResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                    ),
                ),
                ("task_id", models.UUIDField(unique=True)),
                ("celery_name", models.CharField(max_length=255)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("completed", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(default="pending", max_length=30)),
                (
                    "data",
                    models.JSONField(
                        blank=True,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                (
                    "job_kwargs",
                    models.JSONField(
                        blank=True,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Celery Result",
                "verbose_name_plural": "Celery Results",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="CeleryLogEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                (
                    "log_level",
                    models.CharField(db_index=True, default=20, max_length=32),
                ),
                ("grouping", models.CharField(default="main", max_length=100)),
                ("message", models.TextField(blank=True)),
                ("created", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "job_result",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="logs",
                        to="netbox_celery.celeryresult",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Celery Log Entries",
                "ordering": ["created"],
                "get_latest_by": "created",
            },
        ),
    ]
