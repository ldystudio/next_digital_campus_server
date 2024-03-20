from django.db import models
from iam.models import User


class Information(models.Model):
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(
        verbose_name="性别", choices=gender_choices, default=1
    )
    service_date = models.DateField(verbose_name="入职日期", null=True)
    birth_date = models.DateField(verbose_name="出生日期", null=True)
    status_choices = ((1, "在职"), (2, "休假"), (3, "离职"))
    service_status = models.SmallIntegerField(
        verbose_name="在职状态", choices=status_choices, default=1
    )
    identification_number = models.CharField(
        verbose_name="身份证件号码", max_length=20, unique=True, null=True
    )
    address = models.CharField(verbose_name="地址", max_length=100, null=True)
    photograph = models.ImageField(
        verbose_name="照片", upload_to="student_photos/", null=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_information",
        verbose_name="用户",
    )

    # class_name = models.CharField(verbose_name="班级", max_length=50)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "教师信息"
        verbose_name_plural = verbose_name
        ordering = ("-date_joined",)
