from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import token_obtain_pair, token_verify, token_refresh

from . import views

router = SimpleRouter()
# router.register('iam', views.AccountViewSet, basename='iam')
router.register('auth', views.AuthViewSet, basename='auth')

urlpatterns = [
    path('auth/login/', token_obtain_pair, name='token_obtain_pair'),
    path('auth/refresh/', token_refresh, name='token_refresh'),
    path('auth/verify/', token_verify, name='token_verify'),
    path('auth/image_captcha/', views.ImageCaptcha.as_view(), name='captcha1'),
    path('auth/email_captcha/', views.EmailCaptcha.as_view(), name='captcha2'),
    path('test/', views.TestView.as_view(), name='test'),
]

urlpatterns += router.urls
