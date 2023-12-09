from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from django.db.models import Q
from rest_framework import serializers

from iam.models import User


# 自定义身份校验
class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        traceId = request.data.get('traceId')
        login_type = request.data.get('type')
        if login_type == 'emailLogin':
            verCode = request.data.get('emailCaptcha')
            email = request.data.get('email')
            if verCode is None or traceId is None:
                raise serializers.ValidationError('验证码不能为空')

            # 获取缓存中的验证码
            captcha = cache.get(traceId, version='EmailCaptcha')
            # 验证码验证
            if verCode.lower() != captcha.lower():
                raise serializers.ValidationError('验证码错误')
            # 验证码验证成功后，删除缓存
            # cache.expire(traceId, timeout=0, version='EmailCaptcha')

            try:
                # 用户名和邮箱验证
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('邮箱没有注册')
            return user
        else:
            verCode = request.data.get('captcha')
            if verCode is None or traceId is None:
                raise serializers.ValidationError('验证码不能为空')

            # 获取缓存中的验证码
            captcha = cache.get(traceId, version='ImageCaptcha')
            # 验证码验证
            if not captcha or verCode.lower() != captcha.lower():
                raise serializers.ValidationError('验证码错误')
            # 验证码验证成功后，删除缓存
            cache.expire(traceId, timeout=0, version='ImageCaptcha')

            try:
                # 用户名和邮箱验证
                user = User.objects.get(Q(username=username) | Q(email=username))
            except User.DoesNotExist:
                raise serializers.ValidationError('账号没有注册')

            if user.check_password(password):
                return user
            else:
                # 密码错误，送给SimpleJwt报错
                return
