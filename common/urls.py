from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("log", views.APIRequestLogViewSet, basename="api-request-log")
router.register(
    "log/response",
    views.APIRequestLogResponseLogViewSet,
    basename="api-request-log-response",
)
router.register(
    "log/errors",
    views.APIRequestLogErrorsLogViewSet,
    basename="api-request-log-errors",
)

urlpatterns = router.urls
