from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from common.exception.exception import InBlacklist
from common.utils import in_blacklist
from iam.models import User


# 自定义登录认证
class LoginModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        trace_id = request.data.get('traceId')
        login_type = request.data.get('type')
        email = request.data.get('email')

        # if login_type not in ['emailLogin', 'imageLogin']:
        #     raise serializers.ValidationError('Invalid login type')

        ver_code = request.data.get('emailCaptcha' if login_type == 'emailLogin' else 'captcha')
        if ver_code is None or trace_id is None:
            raise serializers.ValidationError('验证码不能为空')

        captcha_type = 'EmailCaptcha' if login_type == 'emailLogin' else 'ImageCaptcha'
        captcha = cache.get(trace_id, version=captcha_type)
        if not captcha or ver_code.lower() != captcha.lower():
            raise serializers.ValidationError('验证码错误')
        cache.expire(trace_id, timeout=0, version=captcha_type)

        try:
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(email=email))
        except User.DoesNotExist:
            raise serializers.ValidationError('账号没有注册')

        if login_type != 'emailLogin' and not user.check_password(password):
            raise serializers.ValidationError('账号或密码错误')

        return user


class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = self.get_token(request)
        if token is None:
            return None

        try:
            validated_token = self.get_validated_token(token)
        except InvalidToken:
            raise exceptions.AuthenticationFailed(_("无效的token"))

        user = self.get_user(validated_token)

        if not user:
            raise exceptions.AuthenticationFailed(_("无效的token"))

        if in_blacklist(validated_token):
            raise InBlacklist(_("token已失效"))

        return user, validated_token

    @staticmethod
    def get_token(request):
        return request.COOKIES.get('accessToken')