import snowflake.client
from django.core.cache import cache
from rest_framework import serializers
from django.db import transaction
from iam.models import User
from student import models as student_models
from teacher import models as teacher_models


class UserSerializer(serializers.ModelSerializer):
    # 查询时将id转为字符串，以防id传输到前端精度丢失
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["id"] = str(ret["id"])
        return ret

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

        user = User.objects.create_user(
            id=snowflake.client.get_guid(),
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            user_role=validated_data["roleType"],
            avatar=validated_data["avatar"],
        )

        user_role = user.user_role
        if user_role == "student":
            # 在事务中执行创建操作，确保两条条数据都创建成功
            with transaction.atomic():
                try:
                    student_models.Information.objects.create(user=user)
                    student_models.Enrollment.objects.create(user=user)
                except Exception as e:
                    # 如果有任何异常发生，回滚事务并返回错误响应
                    transaction.set_rollback(True)
                    raise serializers.ValidationError(e)
        if user_role == "teacher":
            teacher_models.Information.objects.create(user=user)
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
