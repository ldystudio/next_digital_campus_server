from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(
    "information", views.ScoreInformationViewSet, basename="ScoreInformation"
)
# router.register("time", views.CourseTimeViewSet, basename="CourseTime")
# router.register("schedule", views.CourseScheduleViewSet, basename="CourseSchedule")
# router.register("choose", views.CourseChooseViewSet, basename="CourseChoose")
urlpatterns = router.urls
