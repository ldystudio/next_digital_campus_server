from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField

from classes.serializers import ClassInformationSerializer
from common.serializer.filed import MultipleSlugRelatedField
from common.serializers import ForeignKeyUserSerializer, ForeignKeyUserWithAddSerializer
from iam.serializers import UserSimpleSerializer
from .models import Information, Enrollment, Attendance


class StudentInformationSerializer(ForeignKeyUserSerializer):
    class Meta:
        model = Information
        fields = (
            "id",
            "user_id",
            "guardian_name",
            "guardian_phone",
            "photograph",
            "identification_number",
            "birth_date",
            "gender",
            "user",
        )
        read_only_fields = ("id", "date_joined", "date_updated")


class StudentEnrollmentSerializer(ForeignKeyUserSerializer):
    classes_id = serializers.CharField(read_only=True)
    class_name = SlugRelatedField(
        source="classes", slug_field="class_name", read_only=True
    )

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "user_id",
            "classes_id",
            "date_of_admission",
            "date_of_graduation",
            "address",
            "disciplinary_records",
            "enrollment_status",
            "notes",
            "user",
            "class_name",
        )
        read_only_fields = ("id", "date_joined", "date_updated")


class StudentAttendanceSerializer(ForeignKeyUserWithAddSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ("id",)


class StudentAttendanceAllTupleSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    group_length = serializers.IntegerField(read_only=True)

    class Meta:
        model = Attendance
        fields = ("id", "user_id", "date", "group_length")
        read_only_fields = ("id", "user_id")


class StudentSimpleSerializer(ForeignKeyUserSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Information
        fields = ("id", "user")
        read_only_fields = ("id",)


class StudentSimpleDetailSerializer(ForeignKeyUserSerializer):
    id = PrimaryKeyRelatedField(
        source="user.student", read_only=True, pk_field=serializers.CharField()
    )
    user = UserSimpleSerializer(read_only=True)
    class_name = SlugRelatedField(
        source="classes", slug_field="class_name", read_only=True
    )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["enrollment_status"] = instance.get_enrollment_status_display()
        return ret

    class Meta:
        model = Enrollment
        fields = (
            "id",
            "user",
            "date_of_admission",
            "enrollment_status",
            "class_name",
        )
