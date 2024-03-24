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
    class Meta:
        model = Enrollment
        fields = (
            "id",
            "user_id",
            "class_name",
            "date_of_admission",
            "date_of_graduation",
            "address",
            "disciplinary_records",
            "enrollment_status",
            "notes",
            "user",
        )
        read_only_fields = ("id", "date_joined", "date_updated")


class StudentAttendanceSerializer(ForeignKeyUserWithAddSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ("id",)
