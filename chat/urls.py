from django.urls import path
from . import views

urlpatterns = [path("room/", views.RoomAPIView.as_view(), name="Room")]
