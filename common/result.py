from enum import Enum

from rest_framework import status as drf_status
from rest_framework.response import Response


class Status(Enum):
    # 200
    OK_200_SUCCESS = (2000, "查询成功")
    # 201
    OK_201_CREATED = (2010, "创建成功")
    # 202
    OK_202_ACCEPTED = (2020, "更新成功")
    # 203
    OK_203_REFRESH_TOKEN = (2030, "尝试刷新Token")
    # 204
    OK_204_NO_CONTENT = (2040, "删除成功")
    # 400
    FAIL_400_INVALID_PARAM = (4000, "请求参数不匹配")
    FAIL_400_OPERATION = (4001, "操作执行失败")
    # 401
    FAIL_401_AUTHENTICATION = (4010, "用户名或密码错误")
    FAIL_401_INVALID_TOKEN = (4011, "Token无效或已过期")
    FAIL_401_INVALID_ACCOUNT = (4012, "无效的账号")
    # 403
    FAIL_403_NO_PERMISSION = (4030, "无权执行该操作")
    # 404
    FAIL_404_NOT_FOUND = (4040, "请求资源不存在")
    # 408
    FAIL_408_REQUEST_TIMEOUT = (4080, "请求连接超时")
    # 415
    FAIL_415_UNSUPPORTED_MEDIA_TYPE = (4150, "不支持的媒体类型")
    # 422
    FAIL_422_UNPROCESSABLE_ENTITY = (4220, "数据校验不通过")
    # 429
    FAIL_429_TOO_MANY_REQUESTS = (4290, "请求过于频繁")
    # 500
    FAIL_500_INTERNAL_SERVER_ERROR = (5000, "系统异常")
    # 503
    FAIL_503_SERVICE_UNAVAILABLE = (5030, "服务不可用")


class Result(Response):
    def __init__(
        self, data=None, status=None, msg=None, code=None, header=None, exception=False
    ):
        """
        重写 Response ，实现 API 统一返回格式
        :param data: 返回数据
        :param status: http 状态码
        :param msg: 返回消息
        :param code: 返回code码
        :param exception: 是否是异常响应
        """
        super().__init__(None, status=status)
        self.data = {
            "code": code if code is not None else self.get_code(status, exception),
            "msg": msg if msg is not None else self.get_msg(status, exception),
            "data": data,
        }
        if header is not None:
            self.headers = {**self.headers, **header}

    @staticmethod
    def get_code(status, exception):
        """
        获取返回码
        :param status: Http状态码
        :param exception: 是否异常
        :return: 提示码
        """
        if exception:
            return Status.FAIL_500_INTERNAL_SERVER_ERROR.value[0]
        # return status // 100 * 100
        return status * 10

    @staticmethod
    def get_msg(status, exception):
        """
        获取返回信息
        :param status: Http状态码
        :param exception: 是否异常
        :return: 提示信息
        """
        if exception:
            return Status.FAIL_500_INTERNAL_SERVER_ERROR.value[1]
        return (
            "请求成功"
            if status
            in [
                drf_status.HTTP_200_OK,
                drf_status.HTTP_201_CREATED,
                drf_status.HTTP_202_ACCEPTED,
                drf_status.HTTP_204_NO_CONTENT,
            ]
            else "请求失败"
        )

    # 成功响应
    @classmethod
    def OK(cls, data=None, msg=None, code=None, status=drf_status.HTTP_200_OK):
        """
        成功响应的返回信息封装；
        :param data: 需要返回的数据
        :param msg: 返回的消息
        :param code: 返回的code码
        :param status: Http状态码
        :return: Result object
        """
        return cls(code=code, msg=msg, data=data, status=status)

    @classmethod
    def OK_200_SUCCESS(
        cls,
        data=None,
        msg=Status.OK_200_SUCCESS.value[1],
        code=Status.OK_200_SUCCESS.value[0],
    ):
        return cls.OK(code=code, msg=msg, data=data, status=drf_status.HTTP_200_OK)

    @classmethod
    def OK_201_CREATED(
        cls,
        data=None,
        msg=Status.OK_201_CREATED.value[1],
        code=Status.OK_201_CREATED.value[0],
    ):
        return cls.OK(code=code, msg=msg, data=data, status=drf_status.HTTP_201_CREATED)

    @classmethod
    def OK_202_ACCEPTED(
        cls,
        data=None,
        msg=Status.OK_202_ACCEPTED.value[1],
        code=Status.OK_202_ACCEPTED.value[0],
    ):
        return cls.OK(
            code=code, msg=msg, data=data, status=drf_status.HTTP_202_ACCEPTED
        )

    @classmethod
    def OK_203_REFRESH_TOKEN(
        cls,
        data=None,
        msg=Status.OK_203_REFRESH_TOKEN.value[1],
        code=Status.OK_203_REFRESH_TOKEN.value[0],
    ):
        return cls.OK(
            code=code,
            msg=msg,
            data=data,
            status=drf_status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        )

    # 修改、删除
    @classmethod
    def OK_204_NO_CONTENT(
        cls,
        data=None,
        msg=Status.OK_204_NO_CONTENT.value[1],
        code=Status.OK_204_NO_CONTENT.value[0],
    ):
        return cls.OK(
            code=code, msg=msg, data=data, status=drf_status.HTTP_204_NO_CONTENT
        )

    # 失败响应
    @classmethod
    def FAIL(
        cls,
        msg=None,
        code=None,
        data=None,
        status=drf_status.HTTP_400_BAD_REQUEST,
        header=None,
    ):
        """
        失败响应的返回信息封装
        :param header: 需要返回的头信息
        :param data: 需要返回的数据
        :param msg: 返回的消息
        :param code: 返回的code码
        :param status: Http状态码
        :return: Result object
        """
        return cls(data=data, msg=msg, code=code, status=status, header=header)

    @classmethod
    def FAIL_400_INVALID_PARAM(
        cls,
        msg=Status.FAIL_400_INVALID_PARAM.value[1],
        code=Status.FAIL_400_INVALID_PARAM.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code, msg=msg, data=data, status=drf_status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    def FAIL_400_OPERATION(
        cls,
        msg=Status.FAIL_400_OPERATION.value[1],
        code=Status.FAIL_400_OPERATION.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code, msg=msg, data=data, status=drf_status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    def FAIL_401_INVALID_TOKEN(
        cls,
        msg=Status.FAIL_401_INVALID_TOKEN.value[1],
        code=Status.FAIL_401_INVALID_TOKEN.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code, msg=msg, data=data, status=drf_status.HTTP_401_UNAUTHORIZED
        )

    @classmethod
    def FAIL_401_AUTHENTICATION(
        cls,
        msg=Status.FAIL_401_AUTHENTICATION.value[1],
        code=Status.FAIL_401_AUTHENTICATION.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code, msg=msg, data=data, status=drf_status.HTTP_401_UNAUTHORIZED
        )

    @classmethod
    def FAIL_401_INVALID_ACCOUNT(
        cls,
        msg=Status.FAIL_401_INVALID_ACCOUNT.value[1],
        code=Status.FAIL_401_INVALID_ACCOUNT.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code, msg=msg, data=data, status=drf_status.HTTP_401_UNAUTHORIZED
        )

    @classmethod
    def FAIL_403_NO_PERMISSION(
        cls,
        msg=Status.FAIL_403_NO_PERMISSION.value[1],
        code=Status.FAIL_403_NO_PERMISSION.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code, msg=msg, data=data, status=drf_status.HTTP_403_FORBIDDEN
        )

    @classmethod
    def FAIL_404_NOT_FOUND(
        cls,
        msg=Status.FAIL_404_NOT_FOUND.value[1],
        code=Status.FAIL_404_NOT_FOUND.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code, msg=msg, data=data, status=drf_status.HTTP_404_NOT_FOUND
        )

    @classmethod
    def FAIL_408_REQUEST_TIMEOUT(
        cls,
        msg=Status.FAIL_408_REQUEST_TIMEOUT.value[1],
        code=Status.FAIL_408_REQUEST_TIMEOUT.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code, msg=msg, data=data, status=drf_status.HTTP_408_REQUEST_TIMEOUT
        )

    @classmethod
    def FAIL_415_UNSUPPORTED_MEDIA_TYPE(
        cls,
        msg=Status.FAIL_415_UNSUPPORTED_MEDIA_TYPE.value[1],
        code=Status.FAIL_415_UNSUPPORTED_MEDIA_TYPE.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code,
            msg=msg,
            data=data,
            status=drf_status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        )

    @classmethod
    def FAIL_422_UNPROCESSABLE_ENTITY(
        cls,
        msg=Status.FAIL_422_UNPROCESSABLE_ENTITY.value[1],
        code=Status.FAIL_422_UNPROCESSABLE_ENTITY.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code,
            msg=msg,
            data=data,
            status=drf_status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @classmethod
    def FAIL_429_TOO_MANY_REQUESTS(
        cls,
        msg=Status.FAIL_429_TOO_MANY_REQUESTS.value[1],
        code=Status.FAIL_429_TOO_MANY_REQUESTS.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code, msg=msg, data=data, status=drf_status.HTTP_429_TOO_MANY_REQUESTS
        )

    @classmethod
    def FAIL_500_INTERNAL_SERVER_ERROR(
        cls,
        msg=Status.FAIL_500_INTERNAL_SERVER_ERROR.value[1],
        code=Status.FAIL_500_INTERNAL_SERVER_ERROR.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code,
            msg=msg,
            data=data,
            status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @classmethod
    def FAIL_503_SERVICE_UNAVAILABLE(
        cls,
        msg=Status.FAIL_503_SERVICE_UNAVAILABLE.value[1],
        code=Status.FAIL_503_SERVICE_UNAVAILABLE.value[0],
        data=None,
    ):
        return cls.FAIL(
            code=code,
            msg=msg,
            data=data,
            status=drf_status.HTTP_503_SERVICE_UNAVAILABLE,
        )
