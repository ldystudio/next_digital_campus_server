from rest_framework import serializers

from classes.serializers import ClassInformationSerializer
from teacher.serializers import TeacherSimpleSerializer
from .models import Setting, Time


class CourseSettingSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    teacher = TeacherSimpleSerializer(many=True, read_only=True)
    classes = ClassInformationSerializer(many=True, read_only=True)
    course_picture = serializers.ImageField(
        label="课程图片",
        max_length=256,  # 图片名最大长度
        use_url=True,  # 设为True则URL字符串值将用于输出表示。设为False则文件名字符串值将用于输出表示
        error_messages={"invalid": "图片参数错误"},
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Setting
        exclude = ("date_joined", "date_updated")
        read_only_fields = ("id", "date_joined", "date_updated")


class CourseTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        exclude = ("date_joined", "date_updated")
        read_only_fields = ("id", "date_joined", "date_updated")


class CourseChooseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    teacher = TeacherSimpleSerializer(many=True, read_only=True)
    course_picture = serializers.ImageField(
        label="课程图片",
        max_length=256,  # 图片名最大长度
        use_url=True,  # 设为True则URL字符串值将用于输出表示。设为False则文件名字符串值将用于输出表示
        error_messages={"invalid": "图片参数错误"},
        allow_null=True,
        required=False,
    )
    choose_number = serializers.SerializerMethodField()

    def get_choose_number(self, obj):
        return obj.student.count()

    class Meta:
        model = Setting
        fields = (
            "id",
            "course_name",
            "course_description",
            "course_picture",
            "class_location",
            "credit",
            "start_time",
            "end_time",
            "start_date",
            "end_date",
            "weekday",
            "choose_number",
            "teacher",
        )
        read_only_fields = ("id", "date_joined", "date_updated")


class CourseSimpleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Setting
        fields = (
            "id",
            "course_name",
        )
        read_only_fields = ("id",)
