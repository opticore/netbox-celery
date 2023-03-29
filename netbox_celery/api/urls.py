"""URLs for the netbox_celery API."""
from netbox_celery.api.views import CeleryResultView

from netbox.api.routers import NetBoxRouter


router = NetBoxRouter()
router.register("result", CeleryResultView)
urlpatterns = router.urls

app_name = "netbox_celery-api"  # pylint: disable=invalid-name
