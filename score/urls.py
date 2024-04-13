from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register("enter", views.ScoreEnterViewSet, basename="ScoreEnter")
# router.register("time", views.CourseTimeViewSet, basename="CourseTime")
# router.register("schedule", views.CourseScheduleViewSet, basename="CourseSchedule")
# router.register("choose", views.CourseChooseViewSet, basename="CourseChoose")
urlpatterns = router.urls
