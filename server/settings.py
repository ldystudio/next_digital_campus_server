"""
Django's settings for server project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

from generate_rsa_keys import verifying_key, signing_key

try:
    from .local_settings import *
except ImportError:
    raise ImportError("local_settings.py文件未找到或导入失败。请检查Python路径设置确保文件存在。")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_tracking",
    "django_filters",
    "corsheaders",
    "common.apps.CommonConfig",
    "iam.apps.IamConfig",
    "student.apps.StudentConfig",
    "teacher.apps.TeacherConfig",
    "course.apps.CourseConfig",
    "classes.apps.ClassConfig",
    "score.apps.ScoreConfig",
]

MIDDLEWARE = [
    # 跨域中间件要放在最上面
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-Hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "iam.User"
AUTHENTICATION_BACKENDS = ["common.authentication.LoginModelBackend"]

# DRF全局配置
REST_FRAMEWORK = {
    # 认证
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # JWT认证
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 重写JWT认证，加入redis黑名单机制
        "common.authentication.JWTCookieOrHeaderAuthentication",
    ),
    # 权限
    "DEFAULT_PERMISSION_CLASSES": (
        # 仅为认证通过的用户提供访问权限
        "rest_framework.permissions.IsAuthenticated",
    ),
    # 频率
    "DEFAULT_THROTTLE_CLASSES": (
        # 匿名用户频率限制
        # 'rest_framework.throttling.AnonRateThrottle',
        # 用户频率限制
        # 'rest_framework.throttling.UserRateThrottle',
        # 视图频率限制
        # 'rest_framework.throttling.ScopedRateThrottle',
    ),
    # 自定义频率字段与时间
    "DEFAULT_THROTTLE_RATES": {
        # 基于匿名用户的频率限制
        "anon": "100/day",
        # 基于用户的频率限制
        "user": "1000/day",
        # 基于视图的频率限制
        "contacts": "1000/day",
        # 基于上传的频率限制
        "uploads": "20/day",
        # 验证码频率
        "image_captcha": "2/s",
        # 邮箱验证码频率
        "email_captcha": "1/m",
    },
    # 分页
    "DEFAULT_PAGINATION_CLASS": "common.pagination.PageNumberPagination",
    # 过滤
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    # 异常
    "EXCEPTION_HANDLER": "common.exception.handler.exception_handler",
    # 文档
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

REST_FRAMEWORK_EXTENSIONS = {
    "DEFAULT_CACHE_RESPONSE_TIMEOUT": 60 * 15,
}

SIMPLE_JWT = {
    # accessToken有效期
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    # refreshToken有效期
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # 刷新accessToken时是否重新生成refreshToken
    "ROTATE_REFRESH_TOKENS": True,
    # 记录用户最后登录时间
    "UPDATE_LAST_LOGIN": True,
    # 签名算法
    "ALGORITHM": "RS256",
    # 签名密钥
    "SIGNING_KEY": signing_key,
    # 验证密钥
    "VERIFYING_KEY": verifying_key,
    # 用户ID字段
    "USER_ID_CLAIM": "userId",
    # 自定义Token配对序列化器
    "TOKEN_OBTAIN_SERIALIZER": "common.serializer.token.TokenObtainPairSerializer",
    # 自定义Token刷新序列化器
    "TOKEN_REFRESH_SERIALIZER": "common.serializer.token.TokenRefreshSerializer",
}

# CORS跨域配置
# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True

API_VERSION = "api/v1/"
