from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    user_type = models.CharField('用户类型', max_length=12, default='soybean')
    auth_type = models.CharField('认证类型', max_length=5, default='PWD')
    auth_account = models.CharField('身份类型', max_length=10, default='user')
    status_choices = (
        (1, '启用'),
        (2, '禁用'),
        (3, '冻结'),
        (4, '软删除'),
    )
    status = models.SmallIntegerField('状态', choices=status_choices, default=1)
    avatar = models.ImageField(upload_to='iam/avatar/', null=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '账号信息'
        verbose_name_plural = verbose_name
        ordering = ('-date_joined',)
