from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    real_name = models.CharField(verbose_name='真实姓名', max_length=20, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    phone = models.CharField(verbose_name='手机号', max_length=11, null=True)
    email = models.EmailField(verbose_name='邮箱', unique=True, null=True)
    user_role = models.CharField(verbose_name='用户身份', max_length=10, default='student')
    status_choices = ((1, '启用'), (2, '禁用'), (3, '冻结'), (4, '软删除'))
    status = models.SmallIntegerField(
        verbose_name='状态', choices=status_choices, default=1
    )
    avatar = models.CharField(verbose_name='头像', max_length=8, null=True)
    signature = models.CharField(verbose_name='个性签名', max_length=250, null=True)
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(
        verbose_name='性别', choices=gender_choices, default=1
    )
    birth_date = models.DateField(verbose_name='出生日期', null=True)
    address = models.CharField(verbose_name='地址', max_length=100, null=True)

    # avatar = models.ImageField(upload_to='iam/avatar/', null=True)

    class Meta:
        verbose_name = '账号信息'
        verbose_name_plural = verbose_name
        ordering = ('-date_joined',)
