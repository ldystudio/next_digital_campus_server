from common.permissions import IsOwnerAccount
from common.result import Result
from common.viewsets import (
    ReadWriteModelViewSetFormatResult,
    ModelViewSetFormatResult,
    ReadOnlyModelViewSetFormatResult,
)
from iam.serializers import UserSimpleSerializer
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
    TeacherSimpleSerializer,
)
from classes.models import Information as ClassInformation


# Create your views here.
class TeacherInformationViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
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


class TeacherSimpleViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = TeacherSimpleSerializer
    filterset_fields = ("id",)
