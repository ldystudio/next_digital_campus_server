from django.db.models import Q
from django.http.response import Http404
from rest_framework.permissions import IsAuthenticated
from snowflake.client import get_guid

from common.pagination import UnlimitedPagination
from common.permissions import IsOwnerOperation, IsTeacherOrAdminUser
from common.result import Result
from common.utils.decide import is_teacher, is_student
from common.utils.file import file_field_path_delete
from common.utils.foreignKey import foreign_key_fields_update, foreign_key_fields_create
from common.viewsets import (
    ModelViewSetFormatResult,
    ReadOnlyModelViewSetFormatResult,
    ReadWriteModelViewSetFormatResult,
)
from .filters import CourseSettingFilter
from .models import Setting, Time
from .serializers import (
    CourseSettingSerializer,
    CourseTimeSerializer,
    CourseChooseSerializer,
)


# Create your views here.
class CourseSettingsViewSet(ModelViewSetFormatResult):
    queryset = Setting.objects.all().distinct()
    serializer_class = CourseSettingSerializer
    permission_classes = (
        IsTeacherOrAdminUser,
        IsOwnerOperation,
    )
    filterset_class = CourseSettingFilter


def update(self, request, *args, **kwargs):
    partial = kwargs.pop("partial", False)
    try:
        instance = self.get_object()
    except Http404:
        return Result.FAIL_400_INVALID_PARAM(msg="请先创建课程后再上传图片")

    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)

    foreign_key_fields_update(["teacher", "classes"], request.data, instance)
    file_field_path_delete("course_picture", request.data, instance.course_picture)

    self.perform_update(serializer)
    return Result.OK_202_ACCEPTED(data=serializer.data)


def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.validated_data["id"] = get_guid()

    if is_teacher(request):
        teacher = request.user.teacher
        serializer.validated_data["teacher"] = [teacher.id]

    foreign_key_fields_create(["teacher", "classes"], request.data, serializer)

    self.perform_create(serializer)
    return Result.OK_201_CREATED(data=serializer.data)


def perform_create(self, serializer):
    self.delete_cache_by_path_prefix(
        path=["/api/v1/course/schedule/", "/api/v1/course/choose/"]
    )
    super().perform_create(serializer)


def perform_update(self, serializer):
    self.delete_cache_by_path_prefix(
        path=["/api/v1/course/schedule/", "/api/v1/course/choose/"]
    )
    super().perform_update(serializer)


def perform_destroy(self, instance):
    self.delete_cache_by_path_prefix(
        path=["/api/v1/course/schedule/", "/api/v1/course/choose/"]
    )
    super().perform_destroy(instance)


class CourseTimeViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Time.objects.all()
    serializer_class = CourseTimeSerializer
    pagination_class = UnlimitedPagination


class CourseScheduleViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Setting.objects.all().distinct()
    serializer_class = CourseSettingSerializer
    pagination_class = UnlimitedPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        if is_teacher(self.request):
            teacher = self.request.user.teacher
            return queryset.filter(teacher=teacher)

        elif is_student(self.request):
            return queryset.filter(
                Q(classes=self.request.user.student_enrollment.classes)
                | Q(student=self.request.user.student)
            )

        return queryset.none()


class CourseChooseViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Setting.objects.filter(classes=None).distinct()
    serializer_class = CourseChooseSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = CourseSettingFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list" and is_student(self.request):
            return queryset.filter(~Q(student=self.request.user.student))

        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        instance.student.add(request.user.student)

        self.delete_cache_by_path_prefix(path="/api/v1/course/schedule/")
        self.perform_update(serializer)
        return Result.OK_202_ACCEPTED(data=serializer.data)
