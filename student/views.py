from datetime import datetime

from django.db.models import Count, Q
from django.utils import timezone
from pydash import map_
from rest_framework import generics
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_tracking.mixins import LoggingMixin

from common.cache import CacheFnMixin
from common.permissions import IsOwnerOperation, IsStudentOrAdminUser
from common.result import Result
from common.utils.decide import is_teacher, is_student
from common.utils.gain import get_related_field_values_list
from common.viewsets import (
    ReadWriteModelViewSetFormatResult,
    ModelViewSetFormatResult,
    ReadOnlyModelViewSetFormatResult,
)
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
    StudentAttendanceAllTupleSerializer,
    StudentSimpleSerializer,
    StudentSimpleDetailSerializer,
)


# Create your views here.
class StudentInformationViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = StudentInformationSerializer
    filterset_class = StudentInformationFilter
    user_fields = ["real_name", "phone", "email", "avatar"]
    cache_paths_to_delete = [
        "auth/user/",
        "student/enrollment/",
        "student/simple/",
        "student/simple-detail/",
    ]


class StudentEnrollmentViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Enrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    filterset_class = StudentEnrollmentFilter
    user_fields = ["real_name"]
    cache_paths_to_delete = [
        "auth/user/",
        "student/information/",
        "student/simple/",
        "student/simple-detail/",
    ]


class StudentAttendanceViewSet(ModelViewSetFormatResult):
    queryset = Attendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    filterset_class = StudentAttendanceFilter
    cache_paths_to_delete = ["student/attendance-all/"]


class StudentSimpleViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = StudentSimpleSerializer
    filterset_fields = ("id",)

    def get_queryset(self):
        queryset = super().get_queryset()

        if is_teacher(self.request):
            course = self.request.user.teacher.course.all()
            return queryset.filter(
                Q(id__in=get_related_field_values_list(course, "student"))
                | Q(
                    user__student_enrollment__classes__in=self.request.user.teacher.classes.all()
                )
            )

        elif is_student(self.request):
            return queryset.filter(user=self.request.user)

        return queryset


class StudentSimpleDetailViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Enrollment.objects.all()
    serializer_class = StudentSimpleDetailSerializer
    permission_classes = (IsStudentOrAdminUser, IsOwnerOperation)

    def get_queryset(self):
        queryset = super().get_queryset()

        if is_student(self.request):
            return queryset.filter(user=self.request.user)

        return queryset

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Result.OK_200_SUCCESS(data=serializer.data)


class StudentTodayAttendanceListView(LoggingMixin, generics.ListAPIView):
    queryset = Attendance.objects.all().filter(
        date=datetime.today().strftime("%Y-%m-%d")
    )
    serializer_class = StudentAttendanceSerializer
    permission_classes = (IsStudentOrAdminUser, IsOwnerOperation)

    logging_methods = ["GET"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)


class StudentAttendanceAllTuplesListView(
    LoggingMixin, CacheFnMixin, generics.ListAPIView
):
    queryset = (
        Attendance.objects.filter(date__year=timezone.now().year)
        .values("date")
        .annotate(group_length=Count("id"))
    )
    serializer_class = StudentAttendanceAllTupleSerializer
    permission_classes = (IsStudentOrAdminUser, IsOwnerOperation)

    logging_methods = ["GET"]

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user_id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        formatted_data = map_(
            serializer.data, lambda data: [data["date"], data["group_length"]]
        )
        return Result.OK_200_SUCCESS(data=formatted_data)
