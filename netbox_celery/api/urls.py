"""URLs for the netbox_celery API."""
from netbox_celery.api.views import CeleryResultView, ResultLogViewSet

from netbox.api.routers import NetBoxRouter


router = NetBoxRouter()
router.register("result", CeleryResultView)
router.register(r'result-logs', ResultLogViewSet, basename="log")
urlpatterns = router.urls

app_name = "netbox_celery-api"  # pylint: disable=invalid-name
