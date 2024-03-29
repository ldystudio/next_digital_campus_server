from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import token_verify

from . import views

router = SimpleRouter()
router.register("user", views.UserViewSet, basename="iam")
router.register("", views.AuthViewSet, basename="auth")
router.register("simple", views.UserSimpleViewSet, basename="simple")

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", token_verify, name="token_verify"),
]

urlpatterns += router.urls
