from rest_framework import serializers
from pydash import pick
import snowflake.client
from common.utils.serializer import validate_user_id_or_real_name
from iam.models import User
from iam.serializers import UserSerializer


class ForeignKeyUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 查询时将id转为字符串，以防id传输到前端精度丢失
        ret["id"] = str(ret["id"])
        # 只保留user中的某些字段
        ret.update(pick(ret.pop("user"), ["real_name", "phone", "email", "avatar"]))
        return ret


class ForeignKeyUserWithAddSerializer(serializers.ModelSerializer):
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
        if request.method in ["PATCH", "PUT"]:
            return attrs

        try:
            user_id = validate_user_id_or_real_name(request)
        except serializers.ValidationError as e:
            raise e

        # 验证user_id是否存在
        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError("用户不存在")

        # 使用snowflake生成的ID
        snowflake_id = snowflake.client.get_guid()

        # 更新attrs字典
        attrs["id"] = snowflake_id
        attrs["user_id"] = user_id

        return attrs
