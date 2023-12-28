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
        f"{token_type}_jti={jti}",
        str(token).split(".")[-1],
        timeout=exp - now,
        version="Blacklist",
    )


def in_blacklist(token):
    token = serializer_token(token)
    token_type, jti = token.payload["token_type"], token.payload["jti"]
    return cache.get(f"{token_type}_jti={jti}", version="Blacklist") is not None


def join_token_caches(token_str, user_id):
    """
    将token加入缓存列表中
    :param token_str: token字符串
    :param user_id: 用户id
    """
    token = serializer_token(token_str)
    token_type, exp = token.payload["token_type"], token.payload["exp"]
    now = datetime_to_epoch(aware_utcnow())
    cache.set(
        f"{token_type}_user_id={user_id}",
        str(token).split(".")[-1],
        timeout=exp - now,
        version=f"{token_type.title()}List",
    )


def in_token_caches(token_str, user_id):
    """
    判断token是否在缓存列表中
    :param token_str: token字符串
    :param user_id: 用户id
    :return: True or False
    """
    token = serializer_token(token_str)
    token_signature = str(token).split(".")[-1]
    token_type = token.payload["token_type"]
    cache_token = cache.get(
        f"{token_type}_user_id={user_id}", version=f"{token_type.title()}List"
    )
    return token_signature == cache_token


def remove_token_caches(token_str, user_id):
    """
    将token移出缓存列表
    :param token_str: token字符串
    :param user_id: 用户id
    """
    token = serializer_token(token_str)
    token_type = token.payload["token_type"]
    cache.expire(
        f"{token_type}_user_id={user_id}",
        timeout=0,
        version=f"{token_type.title()}List",
    )
