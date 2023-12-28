import os

from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.utils import datetime_to_epoch, aware_utcnow


def serializer_token(token):
    if isinstance(token, (RefreshToken, AccessToken)):
        return token
    elif isinstance(token, str):
        if token.split(".")[1].startswith("eyJ0b2tlbl90eXBlIjoicmVmcmVzaCI"):
            return RefreshToken(token)
        elif token.split(".")[1].startswith("eyJ0b2tlbl90eXBlIjoiYWNjZXNzIi"):
            return AccessToken(token)
    else:
        raise TypeError(
            "token must be a str or a instance of RefreshToken or AccessToken"
        )


def join_blacklist(token):
    token = serializer_token(token)
    token_type, jti, exp = (
        token.payload["token_type"],
        token.payload["jti"],
        token.payload["exp"],
    )
    now = datetime_to_epoch(aware_utcnow())
    cache.add(
        token_type + "_jti=" + jti,
        str(token).split(".")[-1],
        timeout=exp - now,
        version="Blacklist",
    )


def in_blacklist(token):
    token = serializer_token(token)
    token_type, jti = token.payload["token_type"], token.payload["jti"]
    return cache.get(token_type + "_jti=" + jti, version="Blacklist") is not None


def join_access_list(token, user_id):
    token = serializer_token(token)
    exp = token.payload["exp"]
    now = datetime_to_epoch(aware_utcnow())
    cache.set(
        "access_user_id=" + str(user_id),
        str(token).split(".")[-1],
        timeout=exp - now,
        version="AccessList",
    )


def in_access_list(token, user_id):
    token = str(serializer_token(token)).split(".")[-1]
    cache_token = cache.get("access_user_id=" + str(user_id), version="AccessList")
    return token == cache_token


def remove_access_list(user_id):
    cache.expire("access_user_id=" + str(user_id), timeout=0, version="AccessList")
