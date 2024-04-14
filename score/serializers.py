from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from common.serializer.filed import MultipleSlugRelatedField
from .models import Enter


class ScoreEnterSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    student_id = PrimaryKeyRelatedField(
        source="student.id", read_only=True, pk_field=serializers.CharField()
    )
    course = MultipleSlugRelatedField(
        read_only=True,
        slug_fields=["course_name"],
        pk_field=serializers.CharField(),
    )
    entered_by = MultipleSlugRelatedField(
        read_only=True, slug_fields=["real_name", "email", "avatar"]
    )
    exam_type = serializers.CharField(source="get_exam_type_display")

    class Meta:
        model = Enter
        exclude = ("student",)
        read_only_fields = ("id", "date_joined", "date_updated")
