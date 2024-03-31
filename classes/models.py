from django.db import models


# Create your models here.
class Information(models.Model):
    class_name = models.CharField(db_comment="班级名称", max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = "班级信息"
        verbose_name_plural = verbose_name
        ordering = ("-date_joined",)
