from rest_framework import serializers

from classes.serializers import ClassInformationSerializer
from common.serializers import ForeignKeyUserSerializer, ForeignKeyUserWithAddSerializer
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
    classes = ClassInformationSerializer()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["class_name"] = ret.pop("classes").get("class_name")
        return ret

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
            "classes",
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
