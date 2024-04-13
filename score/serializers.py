from rest_framework import serializers

from course.serializers import CourseSimpleSerializer
from iam.serializers import UserSimpleSerializer
from student.serializers import StudentSimpleSerializer
from .models import Enter


class ScoreEnterSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    student = StudentSimpleSerializer(read_only=True)
    course = CourseSimpleSerializer(read_only=True)
    entered_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Enter
        fields = "__all__"
        read_only_fields = ("id", "date_joined", "date_updated")
