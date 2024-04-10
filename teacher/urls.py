from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    "information", views.TeacherInformationViewSet, basename="TeacherInformation"
)
router.register("work", views.TeacherWorkViewSet, basename="TeacherWork")
router.register(
    "attendance", views.TeacherAttendanceViewSet, basename="TeacherAttendance"
)
router.register("simple", views.TeacherSimpleViewSet, basename="TeacherSimple")

urlpatterns = [
    path(
        "attendance-today/",
        views.TeacherTodayAttendanceListView.as_view(),
        name="TeacherTodayAttendance",
    ),
    path(
        "attendance-all/",
        views.TeacherAttendanceAllTuplesListView.as_view(),
        name="TeacherAttendanceAllTuples",
    ),
] + router.urls
