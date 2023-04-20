"""Views for the netbox_celery plugin."""
import logging

from django.contrib import messages
from django.shortcuts import redirect, render
from extras.signals import clear_webhooks
from netbox_celery.filtersets import CeleryResultFilterSet
from netbox_celery.forms import CeleryResultFilterSetForm, CeleryTaskForm
from netbox_celery.models import CeleryResult
from netbox_celery.tables import CeleryResultTable
from utilities.exceptions import AbortRequest, PermissionsViolation
from utilities.forms import restrict_form_fields

from netbox.views.generic import (
    ObjectDeleteView,
    ObjectEditView,
    ObjectListView,
    ObjectView
)


class CeleryResultListView(ObjectListView):
    """Celery Result list view."""

    table = CeleryResultTable
    queryset = CeleryResult.objects.all()
    filterset = CeleryResultFilterSet
    filterset_form = CeleryResultFilterSetForm
    action_buttons = ()


class CeleryResultView(ObjectView):
    """Celery Result view."""

    model = CeleryResult
    queryset = CeleryResult.objects.all()

    def get_extra_context(self, request, instance):
        """Add extra context to the view."""
        context = {}
        logs = {}
        for log in instance.logs.all().exclude(grouping="main"):
            if log.grouping not in logs:
                logs[log.grouping] = []
            logs[log.grouping].append(log)
        context["log_groups"] = logs
        context["log_main"] = instance.logs.filter(grouping="main")
        return context


class CeleryResultDeleteView(ObjectDeleteView):
    """Celery Result delete view."""

    model = CeleryResult
    queryset = CeleryResult.objects.all()
    default_return_url = "plugins:netbox_celery:celeryresult_list"


#
# Overwritten views
#


class CeleryTaskAddView(ObjectEditView):
    """Celery Form Task view."""

    queryset = CeleryResult.objects.all()
    template_name = "netbox_celery/celery_task_form.html"
    form = CeleryTaskForm

    def get(self, request, *args, **kwargs):
        """
        GET request handler.

        Args:
            request: The current request
        """
        form = self.form()
        restrict_form_fields(form, request.user)

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger("netbox_celery.views.CeleryFormTaskView")
        form = self.form(data=request.POST, files=request.FILES)
        restrict_form_fields(form, request.user)
        obj = None

        if form.is_valid():
            try:
                obj = form.save(request)

                if obj.status == "failed":
                    messages.error(
                        request,
                        f"Task failed: {obj.logs.latest('created').message}",
                    )
                else:
                    messages.success(request, "Job successfully queued.")

                return redirect(
                    "plugins:netbox_celery:celeryresult_view",
                    pk=obj.pk
                    )

            except (AbortRequest, PermissionsViolation) as error:
                logger.debug(error.message)
                form.add_error(None, error.message)
                clear_webhooks.send(sender=self)

        else:
            logger.debug("Form validation failed")

        return render(
            request,
            self.template_name,
            {
                "object": obj,
                "form": form,
                "return_url": self.get_return_url(request, obj),
                **self.get_extra_context(request, obj),
            },
        )
