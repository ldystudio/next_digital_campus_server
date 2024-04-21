from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from snowflake.client import get_guid

from common.serializer.filed import MultipleSlugRelatedField
from course.models import Setting as Course
from student.models import Information as Student
from .models import Information as Score


class ScoreInformationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = MultipleSlugRelatedField(
        queryset=Course.objects.all(), slug_fields=["course_name"]
    )
    entered_by = MultipleSlugRelatedField(
        read_only=True, slug_fields=["real_name", "email", "avatar"]
    )

    @staticmethod
    def get_student(obj):
        user = obj.student.user
        return {
            "id": f"{obj.student.id}",
            "real_name": user.real_name,
            "email": user.email,
            "avatar": user.avatar,
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["student"] = self.get_student(instance)
        return representation

    def validate(self, attrs):
        request = self.context["request"]
        if request.method == "POST":
            student = attrs.get("student")
            course = attrs.get("course")
            exam_type = request.data.get("exam_type", 1)

            if (
                exam_type != 1
                and Score.objects.filter(
                    student=student, course=course, exam_type=exam_type
                ).exists()
            ):
                raise serializers.ValidationError(
                    f"学生「{student.user.real_name}」已有《{course.course_name}》课程的「{Score.exam_type_choices[exam_type - 1][1]}」的成绩"
                )

            if not Course.objects.filter(id=course.id, student=student).exists():
                raise serializers.ValidationError(
                    f"学生「{student.user.real_name}」未参加《{course.course_name}》课程"
                )

            attrs["id"] = get_guid()

        attrs["entered_by_id"] = request.user.id
        return attrs

    class Meta:
        model = Score
        exclude = ("date_joined", "date_updated")
        read_only_fields = ("id", "date_joined", "date_updated")


class ScoreQuerySerializer(serializers.ModelSerializer):
    course_name = SlugRelatedField(
        source="course", read_only=True, slug_field="course_name"
    )

    class Meta:
        model = Score
        fields = ("course_name", "exam_date", "exam_type", "exam_score")
        read_only_fields = ("id", "date_joined", "date_updated")


class ScoreDataSerializer(serializers.ModelSerializer):
    course = MultipleSlugRelatedField(read_only=True, slug_fields=["course_name"])

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["course"] = "-".join(representation.pop("course").values())
        return representation

    class Meta:
        model = Score
        fields = ("course", "exam_date", "exam_score")
