import smtplib
import traceback

from django.core import exceptions
from rest_framework.exceptions import Throttled
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import exception_handler as drf_exception_handler
from django.db.utils import IntegrityError

from common.result import Result


def exception_handler(exc, context):
    # 其他异常处理逻辑...
    # print(context.get('request').META.get('REMOTE_ADDR'))

    # 自定义异常处理函数
    response = drf_exception_handler(exc, context)

    if response is not None:
        error_msg = ""
        # 如果 DRF 已经提供了处理方法，则直接返回其提供的响应
        if isinstance(response.data, dict):
            error_msg = response.data.get('detail') if response.data.get('detail') is not None else exc.detail

            if isinstance(error_msg, ReturnDict):
                error_msg = '\u3000'.join([(v[0] if '_' in k else f"{k}: {v[0]}") for k, v in error_msg.items()])

            if response.data.get('code') == 'token_not_valid':
                if context['view'].__class__.__name__ == 'TokenRefreshView':
                    response = Result.FAIL_401_INVALID_TOKEN()
                else:
                    response = Result.OK_203_REFRESH_TOKEN()

        if isinstance(response.data, list):
            error_msg = exc.detail[0]

        if isinstance(exc, Throttled):
            response = Result.FAIL_429_TOO_MANY_REQUESTS(error_msg)
        else:
            response = Result.FAIL(code=response.status_code * 10,
                                   msg=error_msg,
                                   status=response.status_code,
                                   header=response.headers)
    else:
        if isinstance(exc, IntegrityError):
            response = Result.FAIL_400_INVALID_PARAM('用户名或邮箱已存在')
        elif isinstance(exc, exceptions.ValidationError):
            response = Result.FAIL_400_INVALID_PARAM(exc.message)
        elif isinstance(exc, smtplib.SMTPDataError):
            response = Result.FAIL_400_INVALID_PARAM("邮箱可能包含不存在的帐户，请检查收件人邮箱。")
        else:
            # 否则，根据需求，自定义异常处理逻辑
            response = Result.FAIL_500_INTERNAL_SERVER_ERROR()

    # print(traceback.format_exception_only(exc.__class__, exc))
    print(traceback.format_exc())
    return response
