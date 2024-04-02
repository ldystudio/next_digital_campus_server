from django.db import models

from teacher.models import Information as TeacherInformation
from student.models import Information as StudentInformation
from classes.models import Information as ClassInformation


class Setting(models.Model):
    course_name = models.CharField(db_comment="课程名称", max_length=100)
    course_description = models.TextField(db_comment="课程描述", null=True, blank=True)
    course_picture = models.ImageField(
        db_comment="课程图片", upload_to="course_picture", null=True, blank=True
    )
    start_time = models.TimeField(db_comment="上课时间")
    end_time = models.TimeField(db_comment="下课时间")
    class_location = models.CharField(db_comment="上课地点", max_length=100)
    credit = models.DecimalField(db_comment="课程学分", max_digits=5, decimal_places=1)
    course_type_choices = ((1, "必修课"), (2, "选修课"), (3, "实践课"))
    course_type = models.SmallIntegerField(
        db_comment="课程类型", choices=course_type_choices, default=1
    )
    enrollment_limit = models.PositiveIntegerField(db_comment="选课人数限制", default=100)
    day_choices = (
        (1, "星期一"),
        (2, "星期二"),
        (3, "星期三"),
        (4, "星期四"),
        (5, "星期五"),
        (6, "星期六"),
        (7, "星期七"),
    )
    weekday = models.IntegerField(db_comment="上课星期", choices=day_choices, default=7)
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
        to=TeacherInformation,
        related_name="course_teacher",
    )
    student = models.ManyToManyField(
        to=StudentInformation,
        related_name="course_student",
        blank=True,
    )
    classes = models.ManyToManyField(
        to=ClassInformation,
        related_name="course_class",
        blank=True,
    )

    def __str__(self):
        return self.course_name

    class Meta:
        verbose_name = "课程设置"
        verbose_name_plural = verbose_name
        ordering = ("-date_joined",)


class Time(models.Model):
    start_time = models.TimeField(db_comment="课程开始时间")
    end_time = models.TimeField(db_comment="课程结束时间")
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}'s start time is {self.start_time} and end date is {self.end_time}"

    class Meta:
        verbose_name = "课程时间"
        verbose_name_plural = verbose_name
        ordering = ("id",)
