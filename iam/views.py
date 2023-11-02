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
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from common.captcha import generate_captcha
from common.result import Result
from common.throttling import ImageCaptchaThrottle, EmailCaptchaThrottle
from common.utils import join_blacklist
from .serializer import RegisterAccountSerializer


class ImageCaptcha(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = (ImageCaptchaThrottle,)

    def get(self, request, *args, **kwargs):
        text, image = generate_captcha()
        out = BytesIO()
        image.save(out, format='png')

        traceId = request.query_params.get('traceId')
        cache.add(traceId, text, timeout=60 * 5, version='ImageCaptcha')

        no_cache_header = {'Pragma': 'no-cache',
                           'Cache-Control': 'no-cache',
                           'Expires': datetime.now(pytz.timezone('GMT')).strftime('%a, %d %b %Y %H:%M:%S GMT')}
        return HttpResponse(out.getvalue(), content_type='image/png', headers=no_cache_header)


class EmailCaptcha(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_classes = (EmailCaptchaThrottle,)

    def post(self, request, *args, **kwargs):
        recipient = request.data.get('email')
        traceId = request.data.get('traceId')
        validate_email(recipient)

        captcha = ''.join(random.sample(string.digits, 6))
        cache.add(traceId, captcha, timeout=60 * 30, version='EmailCaptcha')

        message = f"""
        您的验证码为：{captcha}，请在30分钟内完成填写。
        【Soybean Admin】
        """
        mail.send_mail(subject='验证码',
                       message=message,
                       from_email='1187551003@qq.com',
                       recipient_list=[recipient])
        return Result.OK_200_SUCCESS(msg='验证码发送成功')


class AuthViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    @action(methods=['POST'], detail=False)
    def logout(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if refresh_token is None:
            raise ValidationError({'detail': 'refresh: 该字段是必填项'})

        join_blacklist(refresh_token)

        return Result.OK_204_NO_CONTENT(msg='退出成功')

    @action(methods=['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = RegisterAccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Result.OK_201_CREATED(msg='注册成功')
        else:
            return Result.FAIL_400_OPERATION(data=serializer.errors)

# class AccountViewSet(ModelViewSet):
#     queryset = Account.objects.all().order_by('-date_joined')
#     serializer_class = RegisterAccountSerializer
#
#     def list(self, request, *args, **kwargs):
#         resp = super().list(request, *args, **kwargs)
#         return Result.OK_200_SUCCESS(data=resp.data)
#
#     def create(self, request, *args, **kwargs):
#         resp = super().create(request, *args, **kwargs)
#         return Result.OK_201_CREATED(data=resp.data)
#
#     def retrieve(self, request, *args, **kwargs):
#         resp = super().retrieve(request, *args, **kwargs)
#         return Result.OK_200_SUCCESS(data=resp.data)
#
#     def update(self, request, *args, **kwargs):
#         resp = super().update(request, *args, **kwargs)
#         return Result.OK_202_ACCEPTED(data=resp.data)
#
#     def destroy(self, request, *args, **kwargs):
#         resp = super().destroy(request, *args, **kwargs)
#         return Result.OK_204_NO_CONTENT(data=resp.data)
