from common.viewsets import ReadWriteModelViewSetFormatResult, ModelViewSetFormatResult
from .filters import (
    StudentInformationFilter,
    StudentEnrollmentFilter,
    StudentAttendanceFilter,
)
from .models import Information, Enrollment, Attendance
from .serializers import (
    StudentInformationSerializer,
    StudentEnrollmentSerializer,
    StudentAttendanceSerializer,
)


# Create your views here.
class StudentInformationViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = StudentInformationSerializer
    filterset_class = StudentInformationFilter
    user_fields = ["real_name", "phone", "email", "avatar"]


class StudentEnrollmentViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Enrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    filterset_class = StudentEnrollmentFilter
    user_fields = ["real_name"]


class StudentAttendanceViewSet(ModelViewSetFormatResult):
    queryset = Attendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    filterset_class = StudentAttendanceFilter
