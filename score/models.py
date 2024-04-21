from django.db import models

from course.models import Setting as CourseSetting
from iam.models import User
from student.models import Information as StudentInformation


class Information(models.Model):
    exam_date = models.DateField(db_comment="考试日期")
    exam_type_choices = ((1, "平时考试"), (2, "期中考试"), (3, "期末考试"))
    exam_type = models.SmallIntegerField(
        db_comment="考试类型", choices=exam_type_choices, default=1
    )
    exam_score = models.IntegerField(db_comment="考试分数")
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    entered_by = models.ForeignKey(
        db_comment="录入者",
        to=User,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        db_comment="课程",
        to=CourseSetting,
        on_delete=models.CASCADE,
        related_name="score",
    )
    student = models.ForeignKey(
        db_comment="学生",
        to=StudentInformation,
        on_delete=models.CASCADE,
        related_name="score",
    )

    def __str__(self):
        return f"{self.student.id}'s {self.course.course_name} Score: {self.exam_score}"

    class Meta:
        verbose_name = "成绩录入"
        verbose_name_plural = verbose_name
        ordering = ("-exam_date",)
