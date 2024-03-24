from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    real_name = models.CharField(db_comment="真实姓名", max_length=20, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    phone = models.CharField(db_comment="手机号", max_length=11, null=True)
    email = models.EmailField(db_comment="邮箱", unique=True, null=True)
    user_role = models.CharField(db_comment="用户身份", max_length=10, default="student")
    status_choices = ((1, "启用"), (2, "禁用"), (3, "冻结"), (4, "软删除"))
    status = models.SmallIntegerField(
        db_comment="状态", choices=status_choices, default=1
    )
    avatar = models.CharField(db_comment="头像", max_length=8, null=True)
    signature = models.CharField(db_comment="个性签名", max_length=250, null=True)

    class Meta:
        verbose_name = "账号信息"
        verbose_name_plural = verbose_name
        ordering = ("-date_joined",)
