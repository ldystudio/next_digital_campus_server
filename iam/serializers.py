from datetime import datetime

from django.core.cache import cache
from django.db import transaction
from rest_framework import serializers
from snowflake.client import get_guid

from iam.models import User
from student import models as student_models
from teacher import models as teacher_models


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "real_name",
            "email",
            "phone",
            "user_role",
            "status",
            "avatar",
            "signature",
        )
        read_only_fields = ("id", "date_joined", "date_updated")


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    emailCaptcha = serializers.CharField(required=True)
    traceId = serializers.CharField(required=True)
    roleType = serializers.CharField(default="student")
    avatar = serializers.CharField()

    def create(self, validated_data):
        ver_code = validated_data.pop("emailCaptcha")
        trace_id = validated_data.pop("traceId")

        # 获取缓存中的验证码
        captcha = cache.get(trace_id, version="EmailCaptcha")
        # 验证码验证
        if not captcha or ver_code.lower() != captcha.lower():
            raise serializers.ValidationError("验证码错误")
        # 验证码验证成功后，删除缓存
        cache.expire(trace_id, timeout=0, version="EmailCaptcha")

        # 创建用户
        role_type = validated_data["roleType"]
        if role_type == "student":
            today = datetime.now().date()
            four_years_later_date = datetime(today.year + 4, 6, 30).date()

            # 在事务中执行创建操作，确保多条数据都创建成功
            with transaction.atomic():
                try:
                    user = User.objects.create_user(
                        id=get_guid(),
                        username=validated_data["username"],
                        password=validated_data["password"],
                        email=validated_data["email"],
                        user_role=validated_data["roleType"],
                        avatar=validated_data["avatar"],
                    )
                    student_models.Information.objects.create(user=user)
                    student_models.Enrollment.objects.create(
                        user=user,
                        date_of_admission=today.strftime("%Y-%m-%d"),
                        date_of_graduation=four_years_later_date.strftime("%Y-%m-%d"),
                    )
                except Exception as e:
                    # 如果有任何异常发生，回滚事务并返回错误响应
                    transaction.set_rollback(True)
                    raise serializers.ValidationError(e)

        if role_type == "teacher":
            with transaction.atomic():
                try:
                    user = User.objects.create_user(
                        id=get_guid(),
                        username=validated_data["username"],
                        password=validated_data["password"],
                        email=validated_data["email"],
                        user_role=validated_data["roleType"],
                        avatar=validated_data["avatar"],
                    )
                    teacher_models.Information.objects.create(user=user)
                except Exception as e:
                    transaction.set_rollback(True)
                    raise serializers.ValidationError(e)

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


class UserSimpleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "real_name",
            "email",
            "avatar",
        )
        read_only_fields = ("id",)
