from django.db import models

from iam.models import User
from classes.models import Information as ClassInformation


class Information(models.Model):
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(
        db_comment="性别", choices=gender_choices, default=1
    )
    birth_date = models.DateField(db_comment="出生日期", null=True, blank=True)
    guardian_name = models.CharField(
        db_comment="监护人姓名", max_length=100, null=True, blank=True
    )
    guardian_phone = models.CharField(
        db_comment="监护人联系电话", max_length=20, null=True, blank=True
    )

    identification_number = models.CharField(
        db_comment="身份证件号码", max_length=20, null=True, blank=True
    )
    photograph = models.ImageField(
        db_comment="照片", upload_to="student_photos/", null=True, blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="student_information",
        db_comment="用户",
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "学生信息"
        verbose_name_plural = verbose_name
        ordering = ("-date_joined",)


class Enrollment(models.Model):
    date_of_admission = models.DateField(db_comment="入学日期", null=True, blank=True)
    date_of_graduation = models.DateField(db_comment="毕业日期", null=True, blank=True)
    address = models.CharField(db_comment="家庭住址", max_length=100, null=True, blank=True)
    disciplinary_records = models.TextField(db_comment="奖惩记录", default="无")
    status_choices = ((1, "在校"), (2, "休学"), (3, "毕业"))
    enrollment_status = models.SmallIntegerField(
        db_comment="就读状态", choices=status_choices, default=1
    )
    notes = models.TextField(db_comment="备注", null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="student_enrollment",
        db_comment="用户",
    )
    classes = models.ForeignKey(
        to=ClassInformation,
        on_delete=models.CASCADE,
        related_name="class_information",
        db_comment="班级",
    )

    def __str__(self):
        return f"{self.user.real_name}'s Enrollment"

    class Meta:
        verbose_name = "学生学籍"
        verbose_name_plural = verbose_name
        ordering = ("-date_joined",)


class Attendance(models.Model):
    date = models.DateField(db_comment="记录日期", auto_now=True)
    attendance_status_choices = ((1, "出勤"), (2, "迟到"), (3, "早退"), (4, "请假"), (5, "缺勤"))
    attendance_status = models.SmallIntegerField(
        db_comment="考勤状态", choices=attendance_status_choices, default=1
    )
    check_in_time = models.TimeField(db_comment="签到时间", auto_now=True)
    ip_address = models.GenericIPAddressField(db_comment="IP地址", null=True, blank=True)
    leave_start_time = models.DateTimeField(
        db_comment="请假开始时间",
        null=True,
    )
    leave_end_time = models.DateTimeField(
        db_comment="请假结束时间",
        null=True,
    )
    leave_reason = models.TextField(
        db_comment="请假理由",
        null=True,
    )
    notes = models.TextField(db_comment="备注", null=True, blank=True)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="student_attendance",
        db_comment="用户",
    )

    def __str__(self):
        return f"{self.user.real_name}'s Attendance on {self.date}"

    class Meta:
        verbose_name = "学生考勤"
        verbose_name_plural = verbose_name
        ordering = ("-date", "-check_in_time")
