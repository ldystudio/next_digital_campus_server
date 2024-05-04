from django.urls import path
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
    "log/errors", views.APIRequestLogErrorsLogViewSet, basename="api-request-log-errors"
)

urlpatterns = [
    path("dashboard/chart/", views.DashboardChartView.as_view(), name="DashboardChart"),
    path(
        "dashboard/analytics/",
        views.DashboardAnalyticsView.as_view(),
        name="DashboardAnalytics",
    ),
] + router.urls
