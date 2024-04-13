from rest_framework import serializers
from pydash import pick
from snowflake.client import get_guid
from common.utils.gain import get_user_id_from_request
from iam.models import User
from iam.serializers import UserSerializer


class ForeignKeyUserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    user = UserSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 只保留user中的某些字段
        ret.update(pick(ret.pop("user"), ["real_name", "phone", "email", "avatar"]))
        return ret


class ForeignKeyUserWithAddSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 只保留user中的某些字段
        ret.update(pick(ret.pop("user"), ["real_name", "email", "avatar"]))
        return ret

    def validate(self, attrs):
        request = self.context["request"]
        if request.method not in ["PATCH", "PUT"]:
            user_id = get_user_id_from_request(request)

            # 验证user_id是否存在
            if not User.objects.filter(id=user_id).exists():
                raise serializers.ValidationError("用户不存在")

            # 使用snowflake生成的ID
            snowflake_id = get_guid()

            # 更新attrs字典
            attrs["id"] = snowflake_id
            attrs["user_id"] = user_id

        return attrs
