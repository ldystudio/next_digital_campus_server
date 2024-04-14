from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    "information", views.StudentInformationViewSet, basename="StudentInformation"
)
router.register(
    "enrollment", views.StudentEnrollmentViewSet, basename="StudentEnrollment"
)
router.register(
    "attendance", views.StudentAttendanceViewSet, basename="StudentAttendance"
)
router.register("simple", views.StudentSimpleViewSet, basename="StudentSimple")
urlpatterns = [
    path(
        "attendance-today/",
        views.StudentTodayAttendanceListView.as_view(),
        name="StudentTodayAttendance",
    ),
    path(
        "attendance-all/",
        views.StudentAttendanceAllTuplesListView.as_view(),
        name="StudentAttendanceAllTuples",
    ),
] + router.urls
