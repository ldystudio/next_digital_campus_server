from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    "information", views.ClassInformationViewSet, basename="ClassInformation"
)
urlpatterns = router.urls
