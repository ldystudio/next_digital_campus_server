from django.shortcuts import redirect
from django.urls import reverse
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_tracking.mixins import LoggingMixin

from common.cache import CacheFnMixin, cache_admin_user_response
from common.permissions import IsOwnerOperation
from common.result import Result
from common.utils.decide import (
    is_request_mapped_to_view,
    is_admin,
    is_teacher,
)
from iam.models import User


class ReadOnlyModelViewSetFormatResult(
    LoggingMixin, CacheFnMixin, ReadOnlyModelViewSet
):
    logging_methods = ["GET"]

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    @cache_response(key_func="object_cache_key_func")
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)


class RetrieveModelViewSetFormatResult(
    LoggingMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    logging_methods = ["GET"]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)


class ModelViewSetFormatResult(LoggingMixin, CacheFnMixin, ModelViewSet):
    permission_classes = (IsOwnerOperation,)
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    logging_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list":
            if not is_admin(self.request):
                if is_teacher(self.request):
                    teacher = self.request.user.teacher

                    if is_request_mapped_to_view(self.request, "CourseSettingsViewSet"):
                        return queryset.filter(teacher=teacher)

                    elif is_request_mapped_to_view(self.request, "ScoreEnterViewSet"):
                        return queryset.filter(course__teacher=teacher)

                else:
                    return queryset.filter(user=self.request.user)

        return queryset

    # @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    # @cache_response(key_func="object_cache_key_func")
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def create(self, request, *args, **kwargs):
        if is_request_mapped_to_view(
            request, ["StudentAttendanceViewSet", "TeacherAttendanceViewSet"]
        ):
            request.data["ip_address"] = request.META.get("REMOTE_ADDR")
        response = super().create(request, *args, **kwargs)
        return Result.OK_201_CREATED(data=response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Result.OK_202_ACCEPTED(data=response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Result.OK_202_ACCEPTED(msg="删除成功")


class ReadWriteModelViewSetFormatResult(
    LoggingMixin,
    CacheFnMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    permission_classes = (IsOwnerOperation,)
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    logging_methods = ["GET", "PATCH"]
    user_fields = []

    def split_data(self, request_data):
        user_data = {}
        model_data = {}
        for key, value in request_data.items():
            if key in self.user_fields:
                user_data[key] = value
            elif key in self.serializer_class().get_fields():
                model_data[key] = value
        return user_data, model_data

    @cache_admin_user_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        if is_request_mapped_to_view(
            self.request,
            [
                "StudentInformationViewSet",
                "StudentEnrollmentViewSet",
                "TeacherInformationViewSet",
            ],
        ):
            if not is_admin(request):
                try:
                    obj = self.get_queryset().get(user=request.user)
                except self.queryset.model.DoesNotExist:
                    return Result.FAIL_404_NOT_FOUND(msg="实体信息不存在")

                # 若用户不是管理员，则重定向到实体详情页
                retrieve_url = reverse(
                    request.resolver_match.url_name[:-5] + "-detail",
                    kwargs={"pk": obj.pk},
                )
                return redirect(retrieve_url)

        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    @cache_response(key_func="object_cache_key_func")
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        user_data, model_data = self.split_data(request.data)

        if user_data:
            try:
                user = get_object_or_404(User, id=instance.user_id)
            except (User.DoesNotExist, self.get_queryset().model.DoesNotExist):
                return Result.FAIL_404_NOT_FOUND()

            for attr, val in user_data.items():
                setattr(user, attr, val)
            user.save()

        if model_data:
            for attr, val in model_data.items():
                if attr == "classes":  # 如果属性为 classes，则使用 set 方法
                    instance.classes.set(val)
                else:
                    setattr(instance, attr, val)
            instance.save()

        self.perform_update(serializer)

        if "avatar" in request.data:
            return Result.OK_202_ACCEPTED(code=2031, data=serializer.data)

        return Result.OK_202_ACCEPTED(data=serializer.data)
