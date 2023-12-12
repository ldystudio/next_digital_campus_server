from rest_framework_simplejwt.authentication import JWTAuthentication as SimpleJwtAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from common.exception.exception import InBlacklist
from common.utils import in_blacklist
from common.backends import JWTCookieAuthentication


class JWTAuthentication(JWTCookieAuthentication):

    def authenticate(self, request):
        try:
            user, token = super().authenticate(request)
        except TypeError:
            raise InvalidToken()

        if in_blacklist(token):
            raise InBlacklist()

        return user, token
