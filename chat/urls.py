from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("room", views.RoomViewSet, basename="room")
router.register("message", views.MessageViewSet, basename="message")
urlpatterns = router.urls
