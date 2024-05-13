from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("room", views.RoomViewSet, basename="room")
urlpatterns = router.urls
