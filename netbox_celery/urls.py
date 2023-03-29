"""Netbox Celery Urls."""
from django.urls import path

from netbox_celery.views import (
    CeleryResultDeleteView,
    CeleryResultListView,
    CeleryResultView,
)


urlpatterns = [
    path("celery_results/", CeleryResultListView.as_view(), name="celeryresult_list"),
    path("celery_result/<int:pk>/", CeleryResultView.as_view(), name="celeryresult_view"),
    path(
        "celery_result/<int:pk>/delete/",
        CeleryResultDeleteView.as_view(),
        name="celeryresult_delete",
    ),
]
