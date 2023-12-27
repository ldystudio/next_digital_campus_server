from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_verify,
    token_refresh,
)

from . import views

router = SimpleRouter()
router.register('user', views.UserViewSet, basename='iam')
router.register('', views.AuthViewSet, basename='auth')

urlpatterns = [
    path('login/', token_obtain_pair, name='token_obtain_pair'),
    path('refresh/', token_refresh, name='token_refresh'),
    path('verify/', token_verify, name='token_verify'),
]

urlpatterns += router.urls
