from django.db import models
from iam.models import User
from classes.models import Information as ClassInformation


class Information(models.Model):
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(
        db_comment="性别", choices=gender_choices, default=1
    )
    service_date = models.DateField(db_comment="入职日期", null=True, blank=True)
    birth_date = models.DateField(db_comment="出生日期", null=True, blank=True)
    status_choices = ((1, "在职"), (2, "休假"), (3, "离职"))
    service_status = models.SmallIntegerField(
        db_comment="在职状态", choices=status_choices, default=1
    )
    identification_number = models.CharField(
        db_comment="身份证件号码", max_length=20, unique=True, null=True, blank=True
    )
    address = models.CharField(db_comment="地址", max_length=100, null=True, blank=True)
    photograph = models.ImageField(
        db_comment="照片", upload_to="student_photos/", null=True, blank=True
    )
    date_joined = models.DateTimeField(db_comment="添加时间", auto_now_add=True)
    date_updated = models.DateTimeField(db_comment="修改时间", auto_now=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_information",
        db_comment="用户",
    )
    classes = models.ManyToManyField(
        to=ClassInformation,
        related_name="teacher_class",
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "教师信息"
        verbose_name_plural = verbose_name
        ordering = ("-date_joined",)


class Work(models.Model):
    work_date = models.DateField(db_comment="工作日期")
    work_time = models.TimeField(db_comment="工作时间")
    course_name = models.CharField(
        db_comment="课程名称", max_length=100, null=True, blank=True
    )
    course_class = models.CharField(
        db_comment="课程班级", max_length=50, null=True, blank=True
    )
    meeting_name = models.CharField(
        db_comment="会议名称", max_length=100, null=True, blank=True
    )
    location = models.CharField(
        db_comment="会议地点", max_length=100, null=True, blank=True
    )
    work_content = models.TextField(db_comment="工作内容", null=True, blank=True)
    notes = models.TextField(db_comment="备注", null=True, blank=True)
    date_joined = models.DateTimeField(db_comment="添加时间", auto_now_add=True)
    date_updated = models.DateTimeField(db_comment="修改时间", auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_work",
        db_comment="关联用户",
    )

    def __str__(self):
        return f"{self.user.real_name}'s Work on {self.work_date}"

    class Meta:
        verbose_name = "工作安排"
        verbose_name_plural = verbose_name
        ordering = ("-date_joined",)


class Attendance(models.Model):
    date = models.DateField(db_comment="记录日期", auto_now=True)
    attendance_status_choices = ((1, "出勤"), (2, "迟到"), (3, "早退"), (4, "请假"), (5, "缺勤"))
    attendance_status = models.SmallIntegerField(
        db_comment="考勤状态", choices=attendance_status_choices, default=1
    )
    check_in_time = models.TimeField(db_comment="签到时间", auto_now=True)
    late_time = models.TimeField(db_comment="迟到时间", null=True, blank=True)
    early_leave_time = models.TimeField(db_comment="早退时间", null=True, blank=True)
    leave_start_time = models.DateTimeField(db_comment="请假开始时间", null=True, blank=True)
    leave_end_time = models.DateTimeField(db_comment="请假结束时间", null=True, blank=True)
    leave_reason = models.TextField(db_comment="请假理由", null=True, blank=True)
    notes = models.TextField(db_comment="备注", null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_attendance",
        db_comment="用户",
    )

    def __str__(self):
        return f"{self.user.real_name}'s Attendance on {self.date}"

    class Meta:
        verbose_name = "教师考勤"
        verbose_name_plural = verbose_name
        ordering = ("-date",)
