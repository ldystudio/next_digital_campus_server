from common.viewsets import ReadWriteModelViewSetFormatResult, ModelViewSetFormatResult
from .filters import (
    TeacherInformationFilter,
    TeacherAttendanceFilter,
    TeacherWorkFilter,
)
from .models import Information, Attendance, Work
from .serializers import (
    TeacherInformationSerializer,
    TeacherAttendanceSerializer,
    TeacherWorkSerializer,
)


# Create your views here.
class TeacherInformationViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = TeacherInformationSerializer
    filterset_class = TeacherInformationFilter
    user_fields = ["real_name", "phone", "email", "avatar"]


class TeacherWorkViewSet(ModelViewSetFormatResult):
    queryset = Work.objects.all()
    serializer_class = TeacherWorkSerializer
    filterset_class = TeacherWorkFilter


class TeacherAttendanceViewSet(ModelViewSetFormatResult):
    queryset = Attendance.objects.all()
    serializer_class = TeacherAttendanceSerializer
    filterset_class = TeacherAttendanceFilter
