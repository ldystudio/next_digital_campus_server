from rest_framework import exceptions
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as SimpleJwtTokenObtainPairSerializer,
    TokenRefreshSerializer as SimpleJwtTokenRefreshSerializer,
)

from common.result import Status
from common.utils.token import (
    in_token_caches,
    join_token_caches,
    serializer_token,
)


class TokenObtainPairSerializer(SimpleJwtTokenObtainPairSerializer):
    default_error_messages = {"no_active_account": "用户名或密码错误"}

    @classmethod
    def get_token(cls, user):
        """
        重写get_token方法，往token添加自定义数据
        :param user: 用戶信息
        :return: token
        """
        token = super().get_token(user)
        # 添加个人信息
        token["userId"] = str(user.id)
        token["userName"] = user.username
        token["userRole"] = user.user_role
        token["avatar"] = user.avatar
        return token

    def validate(self, attrs):
        """
        重写validate方法，将token放入缓存
        :param attrs: 用户提交的数据
        :return: 返回数据
        """
        access_and_refresh = super().validate(attrs)
        access_token = access_and_refresh.get("access")
        refresh_token = access_and_refresh.get("refresh")

        join_token_caches(access_token, self.user.id)
        join_token_caches(refresh_token, self.user.id)

        return {
            "code": Status.OK_200_SUCCESS.value[0],
            "msg": "登录成功",
            "data": {"accessToken": access_token, "refreshToken": refresh_token},
        }


class TokenRefreshSerializer(SimpleJwtTokenRefreshSerializer):
    def validate(self, attrs):
        """
        重写validate方法，判断refreshToken是否过期
        :param attrs: 用户提交的数据
        :return: 返回数据
        """

        data = super().validate(attrs)

        old_refresh_token = attrs["refresh"]
        user_id = serializer_token(old_refresh_token).payload.get("userId")

        if not in_token_caches(old_refresh_token, user_id):
            raise exceptions.AuthenticationFailed("refreshToken已失效，请重新登录")

        access_token = data["access"]
        refresh_token = data["refresh"]

        join_token_caches(access_token, user_id)
        join_token_caches(refresh_token, user_id)

        return {
            "code": Status.OK_200_SUCCESS.value[0],
            "msg": "刷新成功",
            "data": {"accessToken": access_token, "refreshToken": refresh_token},
        }
