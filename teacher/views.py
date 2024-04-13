from datetime import datetime

from django.db.models import Count
from django.utils import timezone
from pydash import map_
from rest_framework import generics
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_tracking.mixins import LoggingMixin

from common.cache import CacheFnMixin
from common.permissions import IsOwnerOperation, IsAdminOrTeacherUser
from common.result import Result
from common.utils.decide import is_admin, is_teacher
from common.viewsets import (
    ReadWriteModelViewSetFormatResult,
    ModelViewSetFormatResult,
    ReadOnlyModelViewSetFormatResult,
)
from teacher.models import Information as TeacherInformation
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
    TeacherAttendanceAllTupleSerializer,
)


# Create your views here.
class TeacherInformationViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
    serializer_class = TeacherInformationSerializer
    filterset_class = TeacherInformationFilter
    user_fields = ["real_name", "phone", "email", "avatar"]

    def perform_update(self, serializer):
        self.delete_cache_by_path_prefix(
            path=f"/api/v1/auth/user/{self.request.user.id}"
        )
        super().perform_update(serializer)


class TeacherWorkViewSet(ModelViewSetFormatResult):
    queryset = Work.objects.all()
    serializer_class = TeacherWorkSerializer
    filterset_class = TeacherWorkFilter


class TeacherAttendanceViewSet(ModelViewSetFormatResult):
    queryset = Attendance.objects.all()
    serializer_class = TeacherAttendanceSerializer
    filterset_class = TeacherAttendanceFilter

    def perform_create(self, serializer):
        self.delete_cache_by_path_prefix(path="/api/v1/teacher/attendance-all/")
        super().perform_update(serializer)


class TeacherSimpleViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = TeacherSimpleSerializer
    permission_classes = (IsAdminOrTeacherUser,)
    filterset_fields = ("id",)

    def get_queryset(self):
        queryset = super().get_queryset()

        if is_teacher(self.request):
            teacher = TeacherInformation.objects.get(user=self.request.user)
            return queryset.filter(id=teacher.id)

        return queryset


class TeacherTodayAttendanceListView(LoggingMixin, generics.ListAPIView):
    queryset = Attendance.objects.all().filter(
        date=datetime.today().strftime("%Y-%m-%d")
    )
    serializer_class = TeacherAttendanceSerializer
    permission_classes = (IsOwnerOperation,)

    logging_methods = ["GET"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)


class TeacherAttendanceAllTuplesListView(
    LoggingMixin, CacheFnMixin, generics.ListAPIView
):
    queryset = (
        Attendance.objects.filter(date__year=timezone.now().year)
        .values("date")
        .annotate(group_length=Count("id"))
    )
    serializer_class = TeacherAttendanceAllTupleSerializer
    permission_classes = (IsOwnerOperation,)

    logging_methods = ["GET"]

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user_id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        formatted_data = map_(
            serializer.data, lambda data: [data["date"], data["group_length"]]
        )
        return Result.OK_200_SUCCESS(data=formatted_data)
