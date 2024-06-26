import traceback
from smtplib import SMTPDataError

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import Throttled
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework_simplejwt.exceptions import TokenError
import rest_framework
from common.result import Result
from common.console import console


def exception_handler(exc, context):
    # 其他异常处理逻辑...
    # print(context.get('request').META.get('REMOTE_ADDR'))

    # 自定义异常处理函数
    response = drf_exception_handler(exc, context)

    # 如果 DRF 已经提供了处理方法，则直接返回其提供的响应
    if response:
        error_msg = ""
        if isinstance(response.data, dict):
            error_msg = response.data.get("detail", response.data or exc.detail or exc)

            if isinstance(error_msg, ReturnDict):
                if "non_field_errors" in error_msg:
                    error_msg = error_msg["non_field_errors"][0]
                else:
                    _msg = []

                    for k, v in error_msg.items():
                        if isinstance(v, list):
                            _msg.append(f"{k}: {v[0]}")
                        else:
                            _msg.append(f"{k}: {v}")

                    error_msg = "\u3000".join(_msg)

            if response.data.get("code") == "token_not_valid":
                if context["view"].__class__.__name__ == "TokenRefreshView":
                    response = Result.FAIL_401_INVALID_TOKEN()
                else:
                    response = Result.OK_203_REFRESH_TOKEN()

        if isinstance(response.data, list):
            error_msg = exc.detail[0]

        if isinstance(exc, Throttled):
            response = Result.FAIL_429_TOO_MANY_REQUESTS(
                error_msg.replace("。 Expected available in", "，").replace(
                    "seconds.", "秒后可用。"
                )
            )
        else:
            response = Result.FAIL(
                code=response.status_code * 10,
                msg=error_msg,
                status=response.status_code,
                header=response.headers,
            )
    else:
        # 处理非DRF的异常
        response = handle_validation_errors(exc)

    # print(traceback.format_exception_only(exc.__class__, exc))
    # print(traceback.format_exc())
    console.print_exception(width=150, show_locals=True, suppress=[rest_framework])
    console.rule(title="[bold red]Traceback End", style="red")
    return response


def handle_validation_errors(exc):
    # 映射不同类型的验证错误到相应的处理函数
    validation_errors = {
        IntegrityError: lambda: Result.FAIL_400_INVALID_PARAM("参数错误"),
        ValidationError: lambda: Result.FAIL_400_INVALID_PARAM(exc.message),
        SMTPDataError: lambda: Result.FAIL_400_INVALID_PARAM(
            _("邮箱可能包含不存在的帐户，请检查收件人邮箱。")
        ),
        TokenError: lambda: Result.FAIL_401_INVALID_TOKEN(_("令牌无效或已过期")),
        Http404: lambda: Result.FAIL_404_NOT_FOUND(exc.message),
    }

    # 检查映射中是否有对应的处理函数
    if isinstance(exc, tuple(validation_errors)):
        return validation_errors[exc.__class__]()

    # 默认情况下，处理500内部服务器错误
    return Result.FAIL_500_INTERNAL_SERVER_ERROR()
