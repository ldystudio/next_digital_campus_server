import os

from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.utils import datetime_to_epoch, aware_utcnow


# def is_own_token(refresh, access, user_id):
#     if isinstance(refresh, str):
#         refresh = RefreshToken(refresh)
#     if isinstance(access, str):
#         access = AccessToken(access)
#     return refresh.payload.items() & access.payload.items()
# refresh_payload=refresh.payload
# access_payload=access.payload
# return refresh.payload['userId'] == access.payload['userId'] and \
#     abs(refresh.payload['iat'] - access.payload['iat']) < 10


def in_blacklist(token):
    token = serializer_token(token)
    token_type, jti = token.payload['token_type'], token.payload['jti']
    return cache.get(token_type + '_jti=' + jti, version='Blacklist') is not None


def join_blacklist(token):
    token = serializer_token(token)
    token_type, jti, exp = (
        token.payload['token_type'],
        token.payload['jti'],
        token.payload['exp'],
    )
    now = datetime_to_epoch(aware_utcnow())
    cache.add(
        token_type + '_jti=' + jti,
        str(token).split('.')[-1],
        timeout=exp - now,
        version='Blacklist',
    )


def serializer_token(token):
    if isinstance(token, (RefreshToken, AccessToken)):
        return token
    elif isinstance(token, str):
        if token.split('.')[1].startswith('eyJ0b2tlbl90eXBlIjoicmVmcmVzaCI'):
            return RefreshToken(token)
        elif token.split('.')[1].startswith('eyJ0b2tlbl90eXBlIjoiYWNjZXNzIi'):
            return AccessToken(token)
    else:
        raise TypeError(
            'token must be a str or a instance of RefreshToken or AccessToken'
        )
