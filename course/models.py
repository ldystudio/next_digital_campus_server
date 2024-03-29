from django.db import models

from teacher.models import Information


class Setting(models.Model):
    course_name = models.CharField(db_comment="课程名称", max_length=100)
    course_description = models.TextField(db_comment="课程描述", null=True, blank=True)
    class_time = models.TimeField(db_comment="上课时间")
    class_location = models.CharField(db_comment="上课地点", max_length=100)
    credit = models.DecimalField(db_comment="课程学分", max_digits=5, decimal_places=1)
    course_type_choices = ((1, "必修课"), (2, "选修课"), (3, "实践课"))
    course_type = models.SmallIntegerField(
        db_comment="课程类型", choices=course_type_choices, default=1
    )
    applicable_classes = models.CharField(db_comment="适用班级", max_length=100)
    enrollment_limit = models.PositiveIntegerField(db_comment="选课人数限制", default=1000)
    course_duration = models.CharField(db_comment="课程时长", max_length=50, default="36学时")
    start_date = models.DateField(
        db_comment="课程开始日期",
    )
    end_date = models.DateField(
        db_comment="课程结束日期",
    )
    notes = models.TextField(db_comment="备注", null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    teacher = models.ManyToManyField(
        to=Information,
        related_name="teacher_information",
    )

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = "课程设置"
        verbose_name_plural = verbose_name
        ordering = ("-date_joined",)
