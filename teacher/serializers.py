from rest_framework import serializers

from iam.serializers import UserSimpleSerializer, UserSerializer
from .models import Information, Attendance, Work
from common.serializers import ForeignKeyUserSerializer, ForeignKeyUserWithAddSerializer


class TeacherInformationSerializer(ForeignKeyUserSerializer):
    class Meta:
        model = Information
        exclude = ("date_joined", "date_updated")
        read_only_fields = ("id", "date_joined", "date_updated")


class TeacherWorkSerializer(ForeignKeyUserWithAddSerializer):
    user_id = serializers.CharField(read_only=True)

    class Meta:
        model = Work
        fields = (
            "id",
            "work_date",
            "work_time",
            "course_name",
            "course_class",
            "meeting_name",
            "location",
            "work_content",
            "notes",
            "user",
            "user_id",
        )
        read_only_fields = ("id", "date_joined", "date_updated")


class TeacherAttendanceSerializer(ForeignKeyUserWithAddSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ("id",)


class TeacherSimpleSerializer(ForeignKeyUserSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Information
        fields = ("id", "user")
        read_only_fields = ("id",)
