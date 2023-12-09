import snowflake.client
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.serializers import Serializer

from iam.models import User


class RegisterUserSerializer(Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    emailCaptcha = serializers.CharField(required=True)
    traceId = serializers.CharField(required=True)
    roleType = serializers.CharField(default='student')
    avatar = serializers.CharField()

    def create(self, validated_data):
        ver_code = validated_data.pop('emailCaptcha')
        trace_id = validated_data.pop('traceId')

        # 获取缓存中的验证码
        captcha = cache.get(trace_id, version='EmailCaptcha')
        # 验证码验证
        if not captcha or ver_code.lower() != captcha.lower():
            raise serializers.ValidationError('验证码错误')
        # 验证码验证成功后，删除缓存
        cache.expire(trace_id, timeout=0, version='EmailCaptcha')

        user = User.objects.create_user(
            id=snowflake.client.get_guid(),
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            user_role=validated_data['roleType'],
            avatar=validated_data['avatar']
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
