from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.cache.decorators import cache_response
from snowflake.client import get_guid

from common.pagination import UnlimitedPagination
from common.result import Result
from common.utils.file import file_field_path_delete
from common.utils.foreignKey import foreign_key_fields_update, foreign_key_fields_create
from common.viewsets import (
    ModelViewSetFormatResult,
    ReadOnlyModelViewSetFormatResult,
    ReadWriteModelViewSetFormatResult,
)
from student.models import Enrollment, Information
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
    filterset_class = CourseSettingFilter

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        try:
            instance = self.get_object()
        except Http404:
            return Result.FAIL_404_NOT_FOUND(msg="请先创建课程后再上传图片")
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
        foreign_key_fields_create(["teacher", "classes"], request.data, serializer)
        self.perform_create(serializer)
        return Result.OK_201_CREATED(data=serializer.data)

    def perform_create(self, serializer):
        self.delete_cache_by_path_prefix()
        self.delete_cache_by_path_prefix(
            path=["/api/v1/course/schedule/", "/api/v1/course/choose/"]
        )
        serializer.save()

    def perform_update(self, serializer):
        self.delete_cache_by_path_prefix()
        self.delete_cache_by_path_prefix(
            path=["/api/v1/course/schedule/", "/api/v1/course/choose/"]
        )
        serializer.save()

    def perform_destroy(self, instance):
        self.delete_cache_by_path_prefix()
        self.delete_cache_by_path_prefix(
            path=["/api/v1/course/schedule/", "/api/v1/course/choose/"]
        )
        instance.delete()


class CourseTimeViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Time.objects.all()
    serializer_class = CourseTimeSerializer
    pagination_class = UnlimitedPagination


class CourseScheduleViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Setting.objects.all().distinct()
    serializer_class = CourseSettingSerializer
    pagination_class = UnlimitedPagination

    @cache_response(key_func="list_cache_key_func")
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


class CourseChooseViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Setting.objects.filter(classes=None).distinct()
    serializer_class = CourseChooseSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = CourseSettingFilter

    def get_permissions(self):
        return [permission() for permission in self.permission_classes]

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        student = get_object_or_404(Information, user=request.user)
        queryset = self.filter_queryset(self.get_queryset().filter(~Q(student=student)))
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        paginated_response = self.get_paginated_response(serializer.data)
        return Result.OK_200_SUCCESS(data=paginated_response.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        student = get_object_or_404(Information, user=request.user)
        instance.student.add(student)

        self.delete_cache_by_path_prefix(path="/api/v1/course/schedule/")
        self.perform_update(serializer)
        return Result.OK_202_ACCEPTED(data=serializer.data)
