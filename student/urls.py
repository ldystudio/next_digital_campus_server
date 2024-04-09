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

urlpatterns = [
    path(
        "attendance-today/",
        views.StudentTodayAttendanceGenericsView.as_view(),
        name="StudentTodayAttendance",
    ),
] + router.urls
