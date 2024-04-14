from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from common.serializer.filed import MultipleSlugRelatedField
from student.serializers import StudentSimpleSerializer
from .models import Information


class ScoreInformationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    student = StudentSimpleSerializer(read_only=True)
    course_name = SlugRelatedField(
        source="course", read_only=True, slug_field="course_name"
    )
    entered_by = MultipleSlugRelatedField(
        read_only=True,
        slug_fields=["real_name", "email", "avatar"],
        pk_field=serializers.CharField(),
    )

    class Meta:
        model = Information
        exclude = ("date_joined", "date_updated", "course")
        read_only_fields = ("id", "date_joined", "date_updated")
