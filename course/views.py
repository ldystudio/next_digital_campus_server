from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser

from common.pagination import UnlimitedPagination
from common.result import Result
from common.viewsets import (
    ModelViewSetFormatResult,
    ReadOnlyModelViewSetFormatResult,
    RetrieveUpdateModelViewSetFormatResult,
)
from .filters import CourseSettingFilter
from .models import Setting, Time
from .serializers import (
    CourseSettingSerializer,
    CourseTimeSerializer,
)
from student.models import Enrollment, Information
from django.db.models import Q


# Create your views here.
class CourseSettingsViewSet(ModelViewSetFormatResult):
    queryset = Setting.objects.all().distinct()
    serializer_class = CourseSettingSerializer
    filterset_class = CourseSettingFilter

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # 获取请求中的教师 ID 列表
        teacher_ids = request.data.get("teacher")
        classes_ids = request.data.get("classes")
        # 在保存课程之前，将教师列表中的教师 ID 添加到课程的教师列表中
        if teacher_ids is not None:
            instance.teacher.set(teacher_ids)
        if classes_ids is not None:
            instance.classes.set(classes_ids)
        self.perform_update(serializer)
        return Result.OK_202_ACCEPTED(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取请求中的教师 ID 列表
        teacher_ids = request.data.get("teacher", [])
        classes_ids = request.data.get("classes", [])
        # 在保存课程之前，将教师列表中的教师 ID 添加到课程的教师列表中
        serializer.save(teacher=teacher_ids, classes=classes_ids)
        return Result.OK_201_CREATED(data=serializer.data)


class CourseTimeViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Time.objects.all()
    serializer_class = CourseTimeSerializer
    pagination_class = UnlimitedPagination


class CourseScheduleViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Setting.objects.all()
    serializer_class = CourseSettingSerializer
    pagination_class = UnlimitedPagination

    def list(self, request, *args, **kwargs):
        enrollment = get_object_or_404(Enrollment, user=request.user)
        student = get_object_or_404(Information, user=request.user)
        queryset = self.filter_queryset(
            self.get_queryset().filter(
                Q(classes=enrollment.classes) | Q(student=student)
            )
        )
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        paginated_response = self.get_paginated_response(serializer.data)
        return Result.OK_200_SUCCESS(data=paginated_response.data)


class CourseSelectViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Setting.objects.filter(classes=None)
    serializer_class = CourseSettingSerializer
    pagination_class = UnlimitedPagination
