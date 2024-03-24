from .models import Information, Attendance, Work
from common.serializers import ForeignKeyUserSerializer, ForeignKeyUserWithAddSerializer


class TeacherInformationSerializer(ForeignKeyUserSerializer):
    class Meta:
        model = Information
        fields = (
            "id",
            "user_id",
            "service_date",
            "service_status",
            "photograph",
            "identification_number",
            "birth_date",
            "address",
            "gender",
            "user",
        )
        read_only_fields = ("id", "date_joined", "date_updated")


class TeacherWorkSerializer(ForeignKeyUserWithAddSerializer):
    class Meta:
        model = Work
        exclude = ("date_joined", "date_updated")
        read_only_fields = ("id", "date_joined", "date_updated")


class TeacherAttendanceSerializer(ForeignKeyUserWithAddSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ("id",)
