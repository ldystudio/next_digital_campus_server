from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as SimpleJwtTokenObtainPairSerializer,
    TokenRefreshSerializer as SimpleJwtTokenRefreshSerializer,
)

from common.exception.exception import InBlacklist
from common.result import Status
from common.utils import in_blacklist, join_blacklist


class TokenObtainPairSerializer(SimpleJwtTokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "用户名或密码错误"
    }

    @classmethod
    def get_token(cls, user):
        """
        重写get_token方法，往token添加自定义数据
        :param user: 用戶信息
        :return: token
        """
        token = super().get_token(user)
        # 添加个人信息
        token['userId'] = str(user.id)
        token['userName'] = user.username
        token['userRole'] = user.user_role
        token['realName'] = user.get_full_name()
        token['avatar'] = user.avatar
        token['email'] = user.email
        return token

    def validate(self, attrs):
        """
        重写validate方法，添加自定义返回数据
        :param attrs: 用户提交的数据
        :return: 返回数据
        """
        access_and_refresh = super().validate(attrs)
        data = {
            'accessToken': access_and_refresh.get('access'),
            'refreshToken': access_and_refresh.get('refresh')
        }
        # 获取Token对象
        # refresh = self.get_token(self.user)
        # data['expire'] = refresh.access_token.payload['exp']
        # data['username'] = self.user.username
        # data['email'] = self.user.email
        return {"code": Status.OK_200_SUCCESS.value[0], "msg": "登录成功", "data": data}


class TokenRefreshSerializer(SimpleJwtTokenRefreshSerializer):

    def validate(self, attrs):
        """
        重写validate方法，判断refreshToken是否过期
        :param attrs: 用户提交的数据
        :return: 返回数据
        """
        refresh_token = attrs["refresh"]

        if in_blacklist(refresh_token):
            raise InBlacklist()

        data = super().validate(attrs)

        join_blacklist(refresh_token)
        return {"code": Status.OK_200_SUCCESS.value[0], "msg": "刷新成功",
                "data": {"accessToken": data['access'], "refreshToken": data['refresh']}}
