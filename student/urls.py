from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    "information", views.StudentInformationViewSet, basename="StudentInformation"
)

urlpatterns = router.urls
