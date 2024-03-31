from rest_framework import serializers

from classes.serializers import ClassInformationSerializer
from teacher.serializers import TeacherSimpleSerializer
from .models import Setting, Time


class CourseSettingSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    teacher = TeacherSimpleSerializer(many=True, read_only=True)
    classes = ClassInformationSerializer(many=True, read_only=True)

    class Meta:
        model = Setting
        exclude = ("date_joined", "date_updated")
        read_only_fields = ("id", "date_joined", "date_updated")


class CourseTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        exclude = ("id", "date_joined", "date_updated")
        read_only_fields = ("id", "date_joined", "date_updated")
