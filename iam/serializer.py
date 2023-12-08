import snowflake.client
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.serializers import Serializer

from iam.models import Account


class RegisterAccountSerializer(Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    captcha = serializers.CharField(required=True)
    traceId = serializers.CharField(required=True)

    def create(self, validated_data):
        verCode = validated_data.pop('captcha')
        traceId = validated_data.pop('traceId')

        # 获取缓存中的验证码
        captcha = cache.get(traceId, version='EmailCaptcha')
        # 验证码验证
        if verCode.lower() != captcha.lower():
            raise serializers.ValidationError('验证码错误')
        # 验证码验证成功后，删除缓存
        cache.expire(traceId, timeout=0, version='EmailCaptcha')

        user = Account.objects.create_user(
            id=snowflake.client.get_guid(),
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

    def update(self, instance, validated_data):
        # instance.username = validated_data.get('username', instance.username)
        # instance.email = validated_data.get('email', instance.email)
        # instance.set_password(validated_data.get('password', instance.password))
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        # instance.save()
        # return instance
        pass
