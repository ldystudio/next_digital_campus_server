import snowflake.client
from pydash import pick
from rest_framework import serializers

from iam.models import User
from iam.serializers import UserSerializer
from .models import Information, Enrollment, Attendance


class StudentInformationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 只保留user中的某些字段
        ret.update(pick(ret.pop("user"), ["real_name", "phone", "email", "avatar"]))
        return ret

    class Meta:
        model = Information
        fields = (
            "id",
            "user_id",
            "guardian_name",
            "guardian_phone",
            "photograph",
            "identification_number",
            "birth_date",
            "gender",
            "user",
        )
        read_only_fields = ("id", "date_joined", "date_updated")


class StudentEnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 查询时将id转为字符串，以防id传输到前端精度丢失
        ret["id"] = str(ret["id"])
        # 只保留user中的某些字段
        ret.update(pick(ret.pop("user"), ["real_name", "email", "avatar"]))
        return ret

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "user_id",
            "class_name",
            "date_of_admission",
            "date_of_graduation",
            "address",
            "disciplinary_records",
            "enrollment_status",
            "notes",
            "user",
        )
        read_only_fields = ("id", "date_joined", "date_updated")


class StudentAttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 查询时将id转为字符串，以防id传输到前端精度丢失
        ret["id"] = str(ret["id"])
        # 只保留user中的某些字段
        ret.update(pick(ret.pop("user"), ["real_name", "email", "avatar"]))
        return ret

    def validate(self, attrs):
        request = self.context["request"]
        # 得到user_id
        user_id = request.data.get("user_id") or request.user.id
        # 验证user_id是否存在请求体中
        if not user_id:
            raise serializers.ValidationError("缺少user_id")
        # 验证user_id是否存在
        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError("用户不存在")
        # 设置user_id列的值
        attrs["id"] = snowflake.client.get_guid()
        attrs["user_id"] = user_id
        return attrs

    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ("id",)


# class RegisterUserSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)
#     email = serializers.EmailField(required=True)
#     emailCaptcha = serializers.CharField(required=True)
#     traceId = serializers.CharField(required=True)
#     roleType = serializers.CharField(default="student")
#     avatar = serializers.CharField()
#
#     def create(self, validated_data):
#         ver_code = validated_data.pop("emailCaptcha")
#         trace_id = validated_data.pop("traceId")
#
#         # 获取缓存中的验证码
#         captcha = cache.get(trace_id, version="EmailCaptcha")
#         # 验证码验证
#         if not captcha or ver_code.lower() != captcha.lower():
#             raise serializers.ValidationError("验证码错误")
#         # 验证码验证成功后，删除缓存
#         cache.expire(trace_id, timeout=0, version="EmailCaptcha")
#
#         user = User.objects.create_user(
#             id=snowflake.client.get_guid(),
#             username=validated_data["username"],
#             password=validated_data["password"],
#             email=validated_data["email"],
#             user_role=validated_data["roleType"],
#             avatar=validated_data["avatar"],
#         )
#         return user
#
#     def update(self, instance, validated_data):
#         # instance.username = validated_data.get('username', instance.username)
#         # instance.email = validated_data.get('email', instance.email)
#         # instance.set_password(validated_data.get('password', instance.password))
#         # instance.first_name = validated_data.get('first_name', instance.first_name)
#         # instance.last_name = validated_data.get('last_name', instance.last_name)
#         # instance.save()
#         # return instance
#         pass
