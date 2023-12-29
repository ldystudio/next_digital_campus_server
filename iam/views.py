import random
import string
from datetime import datetime
from io import BytesIO

import pytz
from django.core import mail
from django.core.cache import cache
from django.core.validators import validate_email
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView as SimpleTokenRefreshView,
    TokenObtainPairView,
)
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework_tracking.models import APIRequestLog

from common.authentication import JWTCookieAuthentication
from common.captcha import generate_captcha
from common.permissions import IsOwnerOperation, IsAdminUser
from common.result import Result
from common.throttling import ImageCaptchaThrottle, EmailCaptchaThrottle
from common.utils.token import remove_token_caches, serializer_token
from common.viewsets import ModelViewSetFormatResult
from .models import User
from .serializer import RegisterUserSerializer, UserSerializer


class AuthViewSet(LoggingMixin, ViewSet):
    authentication_classes = []
    permission_classes = []
    logging_methods = ["POST"]

    @action(methods=["GET"], detail=False, throttle_classes=(ImageCaptchaThrottle,))
    def image_captcha(self, request, *args, **kwargs):
        text, image = generate_captcha()
        out = BytesIO()
        image.save(out, format="png")

        trace_id = request.query_params.get("traceId")
        cache.add(trace_id, text, timeout=60 * 5, version="ImageCaptcha")

        no_cache_header = {
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Expires": datetime.now(pytz.timezone("GMT")).strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            ),
        }
        return HttpResponse(
            out.getvalue(), content_type="image/png", headers=no_cache_header
        )

    @action(methods=["POST"], detail=False, throttle_classes=(EmailCaptchaThrottle,))
    def email_captcha(self, request, *args, **kwargs):
        recipient = request.data.get("email")
        trace_id = request.data.get("traceId")
        validate_email(recipient)

        captcha = "".join(random.sample(string.digits, 6))
        cache.add(trace_id, captcha, timeout=60 * 30, version="EmailCaptcha")

        message = f"""
                您的验证码为：{captcha}，请在30分钟内完成填写。
                【Next Digital Campus】
                """
        mail.send_mail(
            subject="验证码",
            message=message,
            from_email="nextdigitalcampus@qq.com",
            recipient_list=[recipient],
        )
        return Result.OK_200_SUCCESS(msg="验证码发送成功")

    @action(
        methods=["POST"], detail=False, authentication_classes=[JWTCookieAuthentication]
    )
    def logout(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        access_token = request.COOKIES.get("accessToken")

        if refresh_token is None:
            raise ValidationError({"detail": "refresh: 该字段是必填项"})

        remove_token_caches(access_token, request.user.id)
        remove_token_caches(refresh_token, request.user.id)

        return Result.OK_204_NO_CONTENT(msg="退出成功")

    @action(methods=["POST"], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Result.OK_201_CREATED(msg="注册成功")
        return Result.FAIL_400_OPERATION(data=serializer.errors)


class LoginView(LoggingMixin, TokenObtainPairView):
    logging_methods = ["POST"]

    def handle_log(self):
        log = APIRequestLog(**self.log)
        log.username_persistent = self.request.data.get("username") or "Anonymous"
        log.save()


class TokenRefreshView(LoggingMixin, SimpleTokenRefreshView):
    logging_methods = ["POST"]

    def handle_log(self):
        log = APIRequestLog(**self.log)
        refresh_token = serializer_token(self.request.data.get("refresh"))
        log.username_persistent = refresh_token.payload.get("userName") or "Anonymous"
        log.save()


class UserViewSet(ModelViewSetFormatResult):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOperation,)

    def get_permissions(self):
        # 仅对“list”操作应用IsAdminUser权限
        return (IsAdminUser(),) if self.action == "list" else super().get_permissions()

    def create(self, request, *args, **kwargs):
        return Result.FAIL_403_NO_PERMISSION(msg="不支持POST请求")
