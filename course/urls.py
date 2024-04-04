from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register("setting", views.CourseSettingsViewSet, basename="CourseSetting")
router.register("time", views.CourseTimeViewSet, basename="CourseTime")
router.register("schedule", views.CourseScheduleViewSet, basename="CourseSchedule")
router.register("select", views.CourseSelectViewSet, basename="CourseSelect")
urlpatterns = router.urls
