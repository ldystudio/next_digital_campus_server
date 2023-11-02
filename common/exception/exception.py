from rest_framework.exceptions import APIException
from rest_framework import status as drf_status
from common.result import Status


class InBlacklist(APIException):
    status_code = drf_status.HTTP_401_UNAUTHORIZED
    default_detail = Status.FAIL_401_INVALID_TOKEN.value[1]
    default_code = 'token_in_blacklist'
